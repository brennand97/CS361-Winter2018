from django.urls import path

from . import views

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'add_dog/', views.add_dog, name='add_dog'),
    path(r'search/<int:zipcode>/', views.search, name='search'),
    path(r'add_dog_to_db/',views.add_dog_to_db, name='add_dog_to_db')
]
