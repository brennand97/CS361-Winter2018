from django.urls import path

from . import views

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'add_dog/', views.add_dog, name='add_dog'),
    path(r'search/<int:zipcode>/', views.search, name='search'),
    path(r'view_listings/', views.view_listings, name='view_listings')
    path(r'shelter_dogs/<str:shelter>/', views.shelter_dogs, name='shelter_dogs')
]
