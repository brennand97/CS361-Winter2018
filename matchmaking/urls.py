from django.urls import path

from . import views

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'search/<int:zipcode>/', views.search, name='search'),
    path(r'add-dog/', views.add_dog, name='add-dog'),
]
