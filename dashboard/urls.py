from django.contrib import admin
from django.urls import path, include

from zone.urls import app_name
from . import views
app_name = 'dashboard'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
]
