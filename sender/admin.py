from django.contrib import admin
from .models import SenderUser , SenderAddress

class SenderUserAdmin(admin.ModelAdmin):
    list_display = ["id", "user",'phone_number']

class SenderAddressAdmin(admin.ModelAdmin):
    list_display = ["id", "user",'address','lat','long']


admin.site.register(SenderUser,SenderUserAdmin)
admin.site.register(SenderAddress,SenderAddressAdmin)