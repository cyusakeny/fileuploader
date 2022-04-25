from django.urls import path
from . import views

urlpatterns = [
    path('files', views.Files, name='files'),
    path('add', views.AddFile, name='Add'),
    path('update/<str:pk>', views.UpdateFile, name='update'),
    path('delete/<str:pk>', views.DeleteFile, name='delete'),
    path('file/<str:pk>', views.GetFile, name='file'),
    path('sharefile/<str:pk>', views.ShareFile, name='sharefile')
]
