from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from carts.admin import CartTabAdmin
from orders.admin import OrderTabularInline

from .models import User

# admin.site.register(User, UserAdmin)

@admin.register(User)
class UserAdminClass(UserAdmin):
    inlines = [CartTabAdmin, OrderTabularInline]