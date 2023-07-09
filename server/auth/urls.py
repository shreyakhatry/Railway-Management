from django.contrib import admin
from django.urls import path

from auth import views

urlpatterns = [
    path('signin/', views.signin),
    path('signup/',views.signup)
]