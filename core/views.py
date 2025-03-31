from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.http import JsonResponse
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .forms import RegisterForm, ThreadForm, ProfileUpdateForm
from .models import Thread, Comment, Profile

# Home page with trending/latest threads and top comments
def home(request):
    trending_threads = Thread.objects.order_by('-views')[:3]
    latest_threads = Thread.objects.order_by('-created_at')[:3]
    top_comments = Comment.objects.annotate(like_count=Count('likes')).order_by('-like_count')[:3]

    return render(request, 'home.html', {
        'trending_threads': trending_threads,
        'latest_threads': latest_threads,
        'top_comments': top_comments
    })

# Register view with password hashing
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            auth_login(request, new_user)
            return redirect('home')
        else:
            messages.error(request, "Registration failed. Please check your input.")
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

# Login view with support for `next` redirect
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

# Logout user
def logout_view(request):
    logout(request)
    return redirect('login')

# Thread list view with optional search and sorting
def thread_list(request):
    threads = Thread.objects.all()
    query = request.GET.get('q')
    sort = request.GET.get('sort')

    if query:
        threads = threads.filter(title__icontains=query)
    if sort == 'latest':
        threads = threads.order_by('-created_at')
    elif sort == 'views':
        threads = threads.order_by('-views')

    from django.core.paginator import Paginator
    paginator = Paginator(threads, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'threads.html', {
        'threads': page_obj,
        'query': query,
        'sort': sort
    })

# Thread detail view with comments
def thread_detail_view(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    thread.views += 1
    thread.save()
    comments = thread.comments.all().order_by('-created_at')
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
            messages.success(request, "Thread created successfully!")
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
@login_required
@require_POST
def ajax_add_comment(request, pk):
    content = request.POST.get('content')
    thread = get_object_or_404(Thread, pk=pk)
    Comment.objects.create(thread=thread, user=request.user, content=content)
    return JsonResponse({'status': 'success'})

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
