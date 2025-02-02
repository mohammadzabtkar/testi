from django.urls import path
from . import views

app_name='zone'
urlpatterns = [
    path('list/', views.zone_list , name="zone_list"),
    path('add/', views.ZoneAddView.as_view() , name="zone_add"),
    path('api/check-point/', views.check_point_in_zone, name='check_point_in_zone'),

]
