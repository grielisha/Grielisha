from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'service', 'status', 'booking_date', 'booking_time', 'total_price', 'created_at')
    list_filter = ('status', 'service', 'created_at')
    search_fields = ('user__email', 'user__username', 'service__name', 'location')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
