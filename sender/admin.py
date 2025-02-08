from django.contrib import admin
from .models import SenderAddress ,SenderProfile



class SenderAddressAdmin(admin.ModelAdmin):
    list_display = ["id", "user",'address','lat','long']


admin.site.register(SenderAddress,SenderAddressAdmin)
admin.site.register(SenderProfile)
