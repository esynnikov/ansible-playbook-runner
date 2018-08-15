from django.urls import re_path, path
from . import views
from .tst_python import glist
from django.views.generic import ListView, DetailView

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
   
]