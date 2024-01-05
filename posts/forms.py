from django import forms
from .models import Post, Comment, Reply

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('user', 'like_users', )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('post', 'user', 'like_users', )
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': '3',
                    'placeholder': '댓글을 입력해주세요',
                }
            ),
        }
        labels = {
            'content': '',
        }


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        exclude = ('user', 'post', 'comment',)
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control mt-2',
                    'rows': '3',
                    'placeholder': '답글을 입력해주세요',
                }
            ),
        }
        labels = {
            'content': '',
        }
        