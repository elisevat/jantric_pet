from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from carts.admin import CartTabAdmin

from .models import User

# admin.site.register(User, UserAdmin)

@admin.register(User)
class UserAdminClass(UserAdmin):
    inlines = [CartTabAdmin,]