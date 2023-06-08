from django.contrib import admin
from Account.models import User_OTP

# Register your models here.
@admin.register(User_OTP)
class User_OTP_admin(admin.ModelAdmin):
    list_display = ( 'get_username', 'get_email', 'otp', 'created_at')

    def get_username(self, obj):
        return obj.user.username
    def get_email(self, obj):
        return obj.user.email
    
    get_username.short_description = 'Username'
    get_email.short_description = 'Email'