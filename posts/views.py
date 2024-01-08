from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Post, Comment, Reply, Category
from accounts.models import User
from .forms import PostForm, CommentForm, ReplyForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
import json
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder

# Create your views here.

def home(request):
    posts = Post.objects.all().order_by('-id')

    context = {
        'posts': posts
    }

    return render(request, 'blogHome/base.html', context)

def detail(request, id):
    post = Post.objects.get(id=id)
    sorted_posts = post.user.post_set.all().order_by('-created_at')
    comment_form = CommentForm()
    reply_form = ReplyForm()
    categories = Category.objects.all()

    context = {
        'post':post,
        'sorted_posts':sorted_posts,
        'comment_form':comment_form,
        'reply_form':reply_form,
        'categories':categories
    }
    return render(request, 'blogDetail/base.html', context)

def catemp(request):
    categories = Category.objects.all()
    if not categories:
        categories = Category()
        categories.category_name = '기본 카테고리'
        categories.save()

    context = {
        'categories': categories,
    }
    return render(request, 'blogDetail/catemp.html', context)

@login_required
def Create_catemp(request):
    category_name = request.POST['categoryName']
    new_category = Category(category_name = category_name)
    new_category.save()

    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return HttpResponseRedirect(reverse('posts:catempPage'))

@login_required
def Update_catemp(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'blogDetail/catempUpdate.html', context)

@login_required
def Delete_catemp(request):
    category_id = request.POST['categoryId']
    delete_category = Category.objects.get(id = category_id)
    delete_category.delete()
    return HttpResponseRedirect(reverse('posts:catempPage'))

@login_required
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('posts:home')
    
    else:
        form = PostForm()
        
    context = {
        'form': form, 
        'categories':categories,
    }

    return render(request, 'form.html', context)


@login_required
def delete(request, id):
    post = Post.objects.get(id=id)
    if request.user == post.user:
        post.delete()

    return redirect('posts:home')


@login_required
def update(request, id):
    post = Post.objects.get(id=id)

    if request.user != post.user:
        return redirect('posts:detail')

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('posts:detail', id=post.id)
    
    else:
        form = PostForm(instance=post)

    context = {
        'form': form
    }

    return render(request, 'form.html', context)

def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('posts:home')
    
    else:
        form = PostForm()

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
        return redirect('posts:home')
    
    if request.method == 'POST':
        comment.content = request.POST.get('comment_content')
        comment.save()
        data = {
        'comment_id': id,
        'post_id': post_id,
    }

    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type = 'application/json')


@login_required
def comment_delete(request, post_id, id):
    comment = Comment.objects.get(id=id)

    if request.user != comment.user:
        return redirect('posts:home')
    
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
        return redirect('posts:home')
    
    else:
        reply.delete()
        data = {
            'reply_id': id,
            'post_id': post_id,
            'comment_id' : comment_id,
        }
    
    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type = 'application/json')


@login_required
def reply_update(request, post_id, comment_id, id):
    reply = Reply.objects.get(id=id)

    if request.user != reply.user:
        return redirect('posts:home')

    if request.method == 'POST':
        reply.content = request.POST.get('reply_content')
        reply.save()
        data = {
        'reply_id': id,
        'post_id': post_id,
        'comment_id' : comment_id,
    }

    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type = 'application/json')