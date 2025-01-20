from django.contrib import admin
from .models import Courier , CourierLocation

class CourierAdmin(admin.ModelAdmin):
    list_display = ["id", "phone_number",'user']
class CourierLocationAdmin(admin.ModelAdmin):
    list_display = ["id", "courier",'latitude','longitude']

admin.site.register(Courier,CourierAdmin)
admin.site.register(CourierLocation,CourierLocationAdmin)