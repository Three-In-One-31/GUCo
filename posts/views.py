from django.shortcuts import render, redirect
from .models import Post, Comment
from accounts.models import User
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http import HttpResponse
import json
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder

# Create your views here.


def index(request):
    posts = Post.objects.all().order_by('-id')
    comment_form = CommentForm()

    context = {
        'posts': posts,
        'comment_form': comment_form,
    }

    return render(request, 'index.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('posts:index')
    
    else:
        form = PostForm()

    context = {
        'form': form
    }

    return render(request, 'form.html', context)


@login_required
def delete(request, id):
    post = Post.objects.get(id=id)
    if request.user == post.user:
        post.delete()

    return redirect('posts:index')


@login_required
def update(request, id):
    post = Post.objects.get(id=id)

    if request.user != post.user:
        return redirect('posts:index')

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('posts:index')
    
    else:
        form = PostForm(instance=post)

    context = {
        'form': form
    }

    return render(request, 'form.html', context)


@login_required
def comment_create(request, post_id):
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.user = request.user
        comment.post_id = post_id
        comment.save()

    return JsonResponse({
                            'id': comment.id,
                            'postId': post_id,
                            'username': comment.user.username,
                            'content': comment.content,
    })


@login_required
def comment_update(request, post_id, id):
    comment = Comment.objects.get(id=id)

    if request.user != comment.user:
        return redirect('posts:index')
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            return redirect('posts:index')

    else:
        form = CommentForm(instance=comment)

    context = {
        'form': form
    }

    return render(request, 'form.html', context)

@login_required
def comment_delete(request, post_id, id):
    comment = Comment.objects.get(id=id)

    if request.user != comment.user:
        return redirect('posts:index')
    
    else:
        comment.delete()
        data = {
            'post_id': post_id,
            'comment_id' : id,
        }

    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type = 'application/json')



@login_required
def likes_async(request, id):
    user = request.user
    post = Post.objects.get(id=id)

    if user in post.like_users.all():
        post.like_users.remove(user)
        status = False

    else:
        post.like_users.add(user)
        status = True

    context = {
        'status': status,
        'count': len(post.like_users.all()),
    }

    return JsonResponse(context)



@login_required
def comment_likes_async(request, post_id, id):
    user = request.user
    post = Post.objects.get(id=post_id)
    comment = Comment.objects.get(id=id)

    if user in comment.like_users.all():
        comment.like_users.remove(user)
        status = False

    else:
        comment.like_users.add(user)
        status = True

    context = {
        'status': status,
        'count': len(comment.like_users.all()),
        'post_id': post.id,
        'comment_id': comment.id,
    }

    return JsonResponse(context)