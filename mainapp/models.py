from django.db import models
from django.contrib.auth.models import User

# Seller profile
class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile')
    company_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='mainapp/sellers/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    
    facebook_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.user.username
    

# Property model
class Property(models.Model):
    PROPERTY_TYPES = (
        ('house', 'House'),
        ('apartment', 'Apartment'),
        ('commercial', 'Commercial'),
        ('land', 'Land'),
    )

    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=200)
    description = models.TextField()
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    location_address = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    image_main = models.ImageField(upload_to='mainapp/properties/')
    image_gallery_1 = models.ImageField(upload_to='mainapp/properties/', blank=True, null=True)
    image_gallery_2 = models.ImageField(upload_to='mainapp/properties/', blank=True, null=True)
    image_gallery_3 = models.ImageField(upload_to='mainapp/properties/', blank=True, null=True)
    amenities = models.TextField(blank=True, null=True)
    floor_plan = models.FileField(upload_to='mainapp/floorplans/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# Favorite properties
class Favorite(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('buyer', 'property')

    def __str__(self):
        return f"{self.buyer.username} favorited {self.property.title}"

# Messages between buyers and sellers
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, blank=True, null=True, related_name='messages')
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient}"

# Buyer profile (optional, for buyer-specific fields like saved searches)
class BuyerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='buyer_profile')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    saved_searches = models.JSONField(blank=True, null=True, help_text='Store buyer search criteria as JSON')
    notification_preferences = models.JSONField(blank=True, null=True, help_text='Store notification preferences as JSON')

    def __str__(self):
        return self.user.username

# Property views tracker
class PropertyView(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='views')
    viewer_ip = models.GenericIPAddressField(blank=True, null=True)
    viewed_at = models.DateTimeField(auto_now_add=True)

# Report model (for admin to review issues)
class Report(models.Model):
    REPORT_TYPES = (
        ('property', 'Property Issue'),
        ('user', 'User Issue'),
    )
    report_type = models.CharField(max_length=50, choices=REPORT_TYPES)
    reported_property = models.ForeignKey(Property, on_delete=models.CASCADE, blank=True, null=True, related_name='reports')
    reported_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='reports')
    reason = models.TextField()
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_made')
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.report_type} report by {self.reported_by.username}"
    
    # models.py
class MeetingRequest(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meeting_requests')
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, related_name='meeting_requests')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, blank=True, null=True)
    message = models.TextField()
    preferred_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email



