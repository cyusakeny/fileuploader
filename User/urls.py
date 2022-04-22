from django.urls import path
from . import views

urlpatterns = [
    path('users', views.UserProfiles, name='users'),
    path('login', views.LoginPage, name='login'),
    path('signup', views.SignUp, name='signup'),
    path('search', views.Search, name='search'),
    path('user/<str:pk>', views.UserProfile, name='user')
]
