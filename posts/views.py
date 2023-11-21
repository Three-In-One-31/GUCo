from django.shortcuts import render, redirect
from .models import Post, Comment, Reply
from accounts.models import User
from .forms import PostForm, CommentForm, ReplyForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Create your views here.


def index(request):
    posts = Post.objects.all().order_by('-id')
    form = CommentForm()
    reply_form = ReplyForm()

    context = {
        'posts': posts,
        'form': form,
        'reply_form': reply_form,
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
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post_id = post_id
        comment.user = request.user
        comment.save()

        return redirect('posts:index')


@login_required
def comment_delete(request, post_id, id):
    comment = Comment.objects.get(id=id)

    if request.user != comment.user:
        return redirect('posts:index')
    
    else:
        comment.delete()

    return redirect('posts:index')


@login_required
def reply_create(request, post_id, comment_id):
    reply_form = ReplyForm(request.POST)
    if reply_form.is_valid():
        reply = reply_form.save(commit=False)
        reply.post_id = post_id
        reply.user = request.user
        reply.comment_id = comment_id
        reply.save()

    return JsonResponse({
                            'id': reply.id,
                            'postId': post_id,
                            'commentId': comment_id,
                            'username': reply.user.username,
                            'content': reply.content,
    })


@login_required
def reply_delete(request, post_id, comment_id, id):
    reply = Reply.objects.get(id=id)

    if request.user != reply.user:
        return redirect('posts:index')
    
    else:
        reply.delete()
    
    return redirect('posts:index')