from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.pre_index, name='pre_index'),
    path('signup/', views.signup, name='signup'),
]