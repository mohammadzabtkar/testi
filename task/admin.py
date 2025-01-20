from django.contrib import admin
from .models import *




class TaskAdmin(admin.ModelAdmin):
    list_display = ["id", "sender",'courier', "destination_user_name",'estimated_price']

class TaskDeliveryLocationAdmin(admin.ModelAdmin):
    list_display = ["id", "task",'latitude', "longitude",'timestamp']

admin.site.register(Task , TaskAdmin)
admin.site.register(TaskDeliveryLocation , TaskDeliveryLocationAdmin)

