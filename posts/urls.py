from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:id>/delete/', views.delete, name='delete'),
    path('<int:id>/update/', views.update, name='update'),

    path('<int:post_id>/comments/create', views.comment_create, name='comment_create'),
    path('<int:post_id>/comments/<int:id>/delete/', views.comment_delete, name='comment_delete'),
    
    path('<int:post_id>/comments/<int:comment_id>/replys/create/', views.reply_create, name='reply_create'),
    path('<int:post_id>/comments/<int:comment_id>/replys/<int:id>/delete/', views.reply_delete, name='reply_delete'),
]