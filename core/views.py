from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST

from .forms import RegisterForm, ThreadForm, ProfileUpdateForm
from .models import Thread, Comment, Profile


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Thread, Comment, Profile

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
            new_user = form.save()
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
            return redirect('home')
        else:
            messages.error(request, 'Invalid Credentials')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def thread_list(request):
    threads = Thread.objects.all()

    query = request.GET.get('q')
    if query:
        threads = threads.filter(title__icontains=query)

    sort = request.GET.get('sort')
    if sort == 'latest':
        threads = threads.order_by('-created_at')
    elif sort == 'views':
        threads = threads.order_by('-views')

    paginator = Paginator(threads, 6)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'threads': page_obj,
        'query': query,
        'sort': sort,
    }

    return render(request, 'threads.html', context)


def about(request):
    return render(request, 'about.html')


def profile_page(request):
    return render(request, 'profile.html')


def ajax_load_trending(request):
    trending = Thread.objects.order_by('-views', '-created_at')[:3]
    data = {
        'trending': [
            {
                'id': t.id,
                'title': t.title,
                'views': t.views,
                'date': t.created_at.strftime("%b %d, %Y")
            }
            for t in trending
        ]
    }
    return JsonResponse(data)


def ajax_load_latest(request):
    latest = Thread.objects.order_by('-created_at')[:3]
    data = {'latest': [{'title': t.title, 'date': t.created_at.strftime("%b %d, %Y")} for t in latest]}
    return JsonResponse(data)


def search_threads(request):
    query = request.GET.get('q', '')
    if query:
        results = Thread.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )[:5]
        data = [{'id': t.id, 'title': t.title} for t in results]
        return JsonResponse({'results': data})
    return JsonResponse({'results': []})


def thread_detail_view(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    thread.views += 1  
    thread.save()
    comments = thread.comments.all().order_by('-created_at')
    return render(request, 'thread_detail.html', {
        'thread': thread,
        'comments': comments
    })


def threads_list_view(request):
    query = request.GET.get('q', '')
    sort = request.GET.get('sort', '')

    threads = Thread.objects.all()

    if query:
        threads = threads.filter(Q(title__icontains=query) | Q(content__icontains=query))

    if sort == 'latest':
        threads = threads.order_by('-created_at')
    elif sort == 'views':
        threads = threads.order_by('-views')

    return render(request, 'threads.html', {'threads': threads, 'query': query, 'sort': sort})


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


def ajax_add_comment(request, pk):
    if request.method == 'POST' and request.user.is_authenticated:
        content = request.POST.get('content')
        thread = get_object_or_404(Thread, pk=pk)
        Comment.objects.create(thread=thread, user=request.user, content=content)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'})


@login_required
def profile_view(request, username):
    user_profile = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=user_profile)
    is_own_profile = request.user == user_profile

    if request.method == 'POST' and is_own_profile:
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            user_profile.username = form.cleaned_data['username']
            user_profile.email = form.cleaned_data['email']
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


@require_POST
def contact_submit(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    message = request.POST.get('message')

    print(f"Contact message from {name} <{email}>: {message}")

    messages.success(request, "Thanks for reaching out! We'll get back to you soon.")
    return redirect('home')
