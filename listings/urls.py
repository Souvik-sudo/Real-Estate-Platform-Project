from django.urls import path
from . import views

urlpatterns = [
    path('', views.property_list, name='property_list'),
    path('search/', views.search_properties, name='search_properties'),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('property/create/', views.property_create, name='property_create'),
    path('search/', views.search_properties, name='search_properties'),
    path('contact/', views.contact, name='contact'),
]
