from django.contrib import admin
from .models import (
    SellerProfile,
    BuyerProfile,
    Property,
    Favorite,
    Message,
    PropertyView,
    Report,
    Booking,
)

# Optional: add a custom admin for better list displays
@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'is_verified')
    search_fields = ('user__username', 'company_name')
    list_filter = ('is_verified',)

@admin.register(BuyerProfile)
class BuyerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')
    search_fields = ('user__username',)

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'property_type', 'price', 'is_available', 'view_count')
    list_filter = ('is_available', 'property_type')
    search_fields = ('title', 'description', 'location_address')
    date_hierarchy = 'created_at'

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'property', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('buyer__username', 'property__title')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'property', 'is_read', 'timestamp')
    list_filter = ('is_read',)
    search_fields = ('sender__username', 'recipient__username', 'content')
    date_hierarchy = 'timestamp'

@admin.register(PropertyView)
class PropertyViewAdmin(admin.ModelAdmin):
    list_display = ('property', 'viewer_ip', 'viewed_at')
    list_filter = ('viewed_at',)
    search_fields = ('viewer_ip', 'property__title')

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_type', 'reported_property', 'reported_user', 'reported_by', 'resolved')
    list_filter = ('resolved', 'report_type')
    search_fields = ('reported_property__title', 'reported_user__username', 'reported_by__username')
    date_hierarchy = 'created_at'


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('property', 'full_name', 'email', 'visit_date', 'visit_time', 'status')
    list_filter = ('status', 'visit_date', 'property')
    search_fields = ('property__title', 'full_name', 'email', 'phone')
    date_hierarchy = 'visit_date'
    ordering = ('-visit_date', '-visit_time')