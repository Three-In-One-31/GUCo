from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('user', 'like_users', )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('post', 'user', 'like_users', )