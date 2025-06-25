from .models import SellerProfile

def seller_profile_context(request):
    seller_profile = SellerProfile.objects.filter(user__is_superuser=True).first()
    return {'seller_profile': seller_profile}
