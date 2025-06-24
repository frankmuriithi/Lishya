from django import forms
from .models import Property, Message, BuyerProfile, SellerProfile, Report
from django.contrib.auth.models import User


# ==================== User Registration Form ====================

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


# ==================== Buyer/Seller Profile ====================

class BuyerProfileForm(forms.ModelForm):
    class Meta:
        model = BuyerProfile
        fields = ['phone_number', 'saved_searches', 'notification_preferences']

class SellerProfileForm(forms.ModelForm):
    class Meta:
        model = SellerProfile
        fields = ['company_name', 'phone_number', 'profile_picture', 'bio']


# ==================== Property Form ====================

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title', 'description', 'property_type', 'price',
            'location_address', 'image_main', 'image_gallery_1',
            'image_gallery_2', 'image_gallery_3', 'amenities', 'floor_plan',
            'is_available'
        ]


# ==================== Message Form ====================

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']


# ==================== Report Form ====================

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['report_type', 'reason', 'reported_property', 'reported_user']
