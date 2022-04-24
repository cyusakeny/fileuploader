from django.urls import path
from . import views

urlpatterns = [
    path('users', views.UserProfiles, name='users'),
    path('login', views.LoginPage, name='login'),
    path('signup', views.SignUp, name='signup'),
    path('search', views.Search, name='search'),
    path('user/<str:pk>', views.UserProfile, name='user'),
    path('reset_password', views.ResetPassword, name='reset password'),
    path('reset_confirm', views.ResetPasswordConfirm, name='Reset password confirm')
]
