from django.contrib import admin
from django.urls import path, include
from . import views
app_name='zone'
urlpatterns = [
    path('list/', views.zone_list , name="zone_list"),
    path('add/', views.zone_add.as_view() , name="zone_add"),
]
