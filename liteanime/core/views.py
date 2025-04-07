from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.http import JsonResponse
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .forms import RegisterForm, ThreadForm, ProfileUpdateForm
from .models import Thread, Comment, Profile, Notification
from django.urls import reverse


def home(request):
    trending_threads = Thread.objects.order_by('-views')[:3]
    latest_threads = Thread.objects.order_by('-created_at')[:3]
    top_comments = Comment.objects.annotate(like_count=Count('likes')).order_by('-like_count')[:3]

    return render(request, 'home.html', {
        'trending_threads': trending_threads,
        'latest_threads': latest_threads,
        'top_comments': top_comments
    })

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            auth_login(request, new_user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next') or 'home'
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid Credentials')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def thread_list(request):
    threads = Thread.objects.annotate(comment_count=Count('comments'))
    query = request.GET.get('q')
    sort = request.GET.get('sort')

    if query:
        threads = threads.filter(title__icontains=query)
    if sort == 'latest':
        threads = threads.order_by('-created_at')
    elif sort == 'views':
        threads = threads.order_by('-views')

    from django.core.paginator import Paginator
    paginator = Paginator(threads, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'threads.html', {
        'threads': page_obj,
        'query': query,
        'sort': sort
    })

def thread_detail_view(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    thread.views += 1
    thread.save()
    comments = thread.comments.filter(parent__isnull=True).order_by('-created_at')
    return render(request, 'thread_detail.html', {
        'thread': thread,
        'comments': comments
    })

# Create new thread (requires login)
@login_required
def create_thread_view(request):
    if request.method == 'POST':
        form = ThreadForm(request.POST, request.FILES)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.user = request.user
            thread.save()
            return redirect('thread_detail', pk=thread.pk)
    else:
        form = ThreadForm()
    return render(request, 'create_thread.html', {'form': form})

# Profile view and update
@login_required
def profile_view(request, username):
    user_profile = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=user_profile)
    is_own_profile = request.user == user_profile

    if request.method == 'POST' and is_own_profile:
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            new_username = form.cleaned_data['username']
            new_email = form.cleaned_data['email']

            if new_username != user_profile.username:
                if User.objects.filter(username=new_username).exclude(pk=user_profile.pk).exists():
                    messages.error(request, "Username already exists.")
                    return redirect('profile', username=user_profile.username)
                user_profile.username = new_username

            if new_email != user_profile.email:
                if User.objects.filter(email=new_email).exclude(pk=user_profile.pk).exists():
                    messages.error(request, "Email already in use.")
                    return redirect('profile', username=user_profile.username)
                user_profile.email = new_email

            user_profile.save()
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile', username=user_profile.username)
    else:
        form = ProfileUpdateForm(instance=profile)
        form.fields['username'].initial = user_profile.username
        form.fields['email'].initial = user_profile.email

    return render(request, 'profile.html', {
        'form': form,
        'user_profile': user_profile,
        'is_own_profile': is_own_profile
    })

# AJAX: Add comment to a thread
@csrf_exempt
@require_POST
@login_required
def ajax_add_comment(request, pk):
    content = request.POST.get("content")
    parent_id = request.POST.get("parent")
    thread = Thread.objects.get(pk=pk)

    if content:
        comment = Comment.objects.create(
            thread=thread,
            user=request.user,
            content=content,
            parent_id=parent_id if parent_id else None
        )

        from core.models import Notification
        from django.urls import reverse

        if thread.user != request.user:
            Notification.objects.create(
                recipient=thread.user,
                sender=request.user,
                message=f"{request.user.username} commented on your thread: {thread.title}",
                url=request.build_absolute_uri(reverse('thread_detail', args=[thread.pk]))
            )

        if parent_id:
            parent_comment = Comment.objects.filter(pk=parent_id).first()
            if parent_comment and parent_comment.user != request.user:
                Notification.objects.create(
                    recipient=parent_comment.user,
                    sender=request.user,
                    message=f"{request.user.username} replied to your comment",
                    url=request.build_absolute_uri(reverse('thread_detail', args=[thread.pk]))
                )

        return JsonResponse({'status': 'success', 'comment_id': comment.id})

    return JsonResponse({'status': 'error', 'message': 'Empty content'})


# AJAX: Load trending threads
def ajax_load_trending(request):
    trending = Thread.objects.order_by('-views', '-created_at')[:3]
    data = {
        'trending': [
            {
                'id': t.id,
                'title': t.title,
                'views': t.views,
                'date': t.created_at.strftime("%b %d, %Y")
            } for t in trending
        ]
    }
    return JsonResponse(data)

# AJAX: Load latest threads
def ajax_load_latest(request):
    latest = Thread.objects.order_by('-created_at')[:3]
    data = {
        'latest': [
            {'title': t.title, 'date': t.created_at.strftime("%b %d, %Y")}
            for t in latest
        ]
    }
    return JsonResponse(data)

# Search threads (used in real-time search)
def search_threads(request):
    query = request.GET.get('q', '')
    if query:
        results = Thread.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))[:5]
        data = [{'id': t.id, 'title': t.title} for t in results]
        return JsonResponse({'results': data})
    return JsonResponse({'results': []})

# About Page
def about(request):
    return render(request, 'about.html')

# Contact Form Submit
@require_POST
def contact_submit(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    message = request.POST.get('message')
    print(f"Contact message from {name} <{email}>: {message}")
    messages.success(request, "Thanks for reaching out! We'll get back to you soon.")
    return redirect('home')

@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')

    if request.method == 'POST':
        notifications.update(is_read=True)
        return redirect('notifications')

    return render(request, 'notifications.html', {'notifications': notifications})