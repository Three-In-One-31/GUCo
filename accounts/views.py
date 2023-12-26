from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .models import User


# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('posts:home')
    else:
        form = CustomUserCreationForm()
    context ={
        'form': form,
    }
    return render(request, 'accounts_form.html', context)


def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            next_url = request.GET.get('next')
            return redirect(next_url or 'posts:home')
    else:
        form = CustomAuthenticationForm()
    context = {
        'form': form, 
    }
    return render(request, 'accounts_form.html', context)


def logout(request):
    auth_logout(request)
    return redirect('posts:home')


def profile(request, username):
    profileuser = User.objects.get(username=username)
    context = {
        'profileuser': profileuser,
    }
    return render(request, 'posts/blogHome/base.html', context)


def follows(request, username):
    me = request.user
    you = User.objects.get(username=username)

    if you in me.followings.all():
        me.followings.remove(you)
    else:
        me.followings.add(you)
    
    return redirect('http://127.0.0.1:8000/posts/', username=username)