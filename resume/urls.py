from unicodedata import name
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="Home"),
    path('contact/', views.contact, name="Contact"),
    path('about/', views.about, name="About"),
]

