from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('<str:username>/', views.profile, name='profile'),
    path('<str:username>/followsHome/', views.followsHome, name='followsHome'),
    # path('<str:username>/followsDetail/', views.followsDetail, name='followsDetail'),
]