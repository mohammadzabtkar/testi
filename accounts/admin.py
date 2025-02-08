from django.contrib import admin
# from .models import CustomUser
#
#
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name",'last_name']
# # Register your models here.
# admin.site.register(CustomUser,CustomUserAdmin)



from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

admin.site.register(CustomUser, UserAdmin)