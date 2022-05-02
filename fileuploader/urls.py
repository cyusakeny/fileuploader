from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='ShowFiles')
urlpatterns = [
    url(r'^$', schema_view),
    path('admin/', admin.site.urls),
    path('', include('projects.urls')),
    path('users/', include('User.urls'))

]
