from django.urls import path

from . import views

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'add_dog/', views.add_dog, name='add_dog')
]
