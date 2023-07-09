from django.urls import re_path, path

from dataaccess import views


urlpatterns = [
    path('clean/', views.truncate_data),
    path('load/', views.load_data),
]