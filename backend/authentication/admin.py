from django.contrib import admin
from .models import Profile, PasswordResetToken 

admin.site.register(Profile)
admin.site.register(PasswordResetToken)