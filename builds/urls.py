from django.urls import re_path, path
from . import views

urlpatterns = [
    re_path(r'^$', views.builds_init, name='builds'),
    re_path(r'^process', views.logprocess, name='builds'),
  
]