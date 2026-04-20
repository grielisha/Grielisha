from django.contrib import admin
from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_type', 'base_price', 'duration_hours', 'is_active', 'created_at')
    list_filter = ('service_type', 'is_active')
    search_fields = ('name', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    actions = ['activate_services', 'deactivate_services']

    def activate_services(self, request, queryset):
        queryset.update(is_active=True)
    activate_services.short_description = "Mark selected services as Active"

    def deactivate_services(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_services.short_description = "Mark selected services as Inactive"

