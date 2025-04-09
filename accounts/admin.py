from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'phone_number']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone_number']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone_number', 'address')}),
    )
