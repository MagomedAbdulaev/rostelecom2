from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {'fields': ('role', 'phone', 'city')}),
    )
    list_display = ('username', 'email', 'role', 'city', 'is_active')
    list_filter = ('role', 'city')

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Object)
class ObjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'address', 'latitude', 'longitude', 'created_at')
    list_filter = ('city',)
    # Делаем поле редактируемым в форме
    fields = ('name', 'city', 'address', 'apartment_number', 'contact_phone',
              'client_portrait', 'services_used', 'current_provider_rating',
              'interested_services', 'convenient_contact_time', 'desired_price',
              'notes', 'latitude', 'longitude', 'status', 'next_contact_date',
              'created_at', 'created_by')

@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'object', 'contact_phone', 'interested_services', 'satisfaction_level')
    list_filter = ('object__city', 'satisfaction_level')
    search_fields = ('name', 'contact_phone', 'notes')

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('engineer', 'client', 'date', 'gps_lat', 'gps_lng')
    list_filter = ('engineer', 'client__object__city', 'date')

@admin.register(ServiceInterest)
class ServiceInterestAdmin(admin.ModelAdmin):
    list_display = ('client', 'service_name', 'interested')
    list_filter = ('interested',)