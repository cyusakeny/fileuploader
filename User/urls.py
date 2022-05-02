from django.urls import path
from . import views

urlpatterns = [
    path('users', views.UserProfiles.as_view(), name='users'),
    path('login', views.LoginPage.as_view(), name='login'),
    path('signup', views.SignUp.as_view(), name='signup'),
    path('search', views.Search, name='search'),
    path('user/<str:pk>', views.UserProfile.as_view(), name='user'),
    path('reset_password', views.ResetPassword.as_view(), name='reset password'),
    path('reset_confirm', views.ResetPasswordConfirm.as_view(), name='Reset password confirm')
]
