from django.urls import path

from . import views

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'add_dog/', views.add_dog, name='add_dog'),
    path(r'search/<int:zipcode>/', views.search, name='search'),
    path(r'view_listings/', views.view_listings, name='view_listings'),
    path(r'shelter_dogs/<str:shelter>/', views.shelter_dogs, name='shelter_dogs'),
    path(r'del_dog/', views.del_dog, name='del_dog'),
    path(r'view_dog/<int:dog_id>/', views.view_dog, name='view_dog'),
    path(r'view_dog/<int:dog_id>/edit/', views.edit_dog, name='edit_dog'),
]
