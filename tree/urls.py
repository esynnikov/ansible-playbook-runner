from django.urls import re_path, path
from . import views

urlpatterns = [
    re_path(r'^$', views.tree_init, name='tree'),
  
]