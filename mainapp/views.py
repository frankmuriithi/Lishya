from datetime import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from .forms import PropertyForm
from django.core.mail import send_mail

from .models import Booking, Property, SellerProfile, Favorite, Message, BuyerProfile, Report, MeetingRequest, Subscriber

# ==================== Authentication Views ====================

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if not all([username, email, first_name, last_name, password, password2]):
            messages.error(request, "Please fill all fields!")
        elif password != password2:
            messages.error(request, "Passwords do not match!")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
        else:
            User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password
            )
            messages.success(request, "Account created successfully! Please log in!")
            return redirect('login')
    return render(request, 'mainapp/register.html')


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        messages.error(request, "Invalid login credentials!")
    return render(request, 'mainapp/login.html')


def user_logout(request):
    logout(request)
    return redirect('index')


# ==================== Public Views ====================

def index(request):
    properties = Property.objects.filter(is_available=True)[:6]
    return render(request, 'mainapp/index.html', {'properties': properties})


def buyers(request):
    """
    Display helpful information for buyers.
    """
    return render(request, 'mainapp/buyers.html')


def about(request):
    """
    Display information about the company, team, values, and mission.
    """
    return render(request, 'mainapp/about.html')


def property_list(request):
    search = request.GET.get('q')
    props = Property.objects.all()
    if search:
        props = props.filter(
            Q(title__icontains=search) |
            Q(location_address__icontains=search) |
            Q(property_type__icontains=search)
        )
    return render(request, 'mainapp/property_list.html', {'properties': props})


def property_detail(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    property_obj.view_count += 1
    property_obj.save()
    return render(request, 'mainapp/property_detail.html', {'property': property_obj})


@login_required
def add_to_favorites(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    Favorite.objects.get_or_create(buyer=request.user, property=prop)
    messages.success(request, "Added to favorites!")
    return redirect('property_list')


@login_required
def view_favorites(request):
    favs = Favorite.objects.filter(buyer=request.user).select_related('property')
    return render(request, 'mainapp/favorites.html', {'favorites': favs})


@login_required

def send_message(request, property_id):
    prop = get_object_or_404(Property, pk=property_id)
    recipient = prop.seller.user
    content = request.POST.get('message')
    if content:
        Message.objects.create(
            sender=request.user,
            recipient=recipient,
            property=prop,
            content=content
        )
        messages.success(request, "Your message was sent!")
    return redirect('property_detail', pk=property_id)


# ==================== Seller Views ====================

@login_required
def seller_dashboard(request):
    profile, _ = SellerProfile.objects.get_or_create(user=request.user)
    properties = profile.properties.all()
    return render(request, 'mainapp/seller_dashboard.html', {'properties': properties})


@login_required
def create_property(request):
    profile, _ = SellerProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        property_type = request.POST.get('property_type')
        location_address = request.POST.get('location_address')
        image_main = request.FILES.get('image_main')
        if title and price:
            Property.objects.create(
                seller=profile,
                title=title,
                description=description,
                price=price,
                property_type=property_type,
                location_address=location_address,
                image_main=image_main
            )
            messages.success(request, "Property created!")
            return redirect('seller_dashboard')
        messages.error(request, "Title and price are required!")
    return render(request, 'mainapp/create_property.html')


@login_required
def edit_property(request, pk):
    prop = get_object_or_404(Property, pk=pk, seller__user=request.user)
    
    if request.method == "POST":
        form = PropertyForm(request.POST, request.FILES, instance=prop)
        if form.is_valid():
            form.save()
            messages.success(request, "Property updated!")
            return redirect('seller_dashboard')
    else:
        form = PropertyForm(instance=prop)
    
    # ✅ Always return a response
    return render(request, 'mainapp/edit_property.html', {'form': form})


@login_required
def mark_as_sold(request, pk):
    prop = get_object_or_404(Property, pk=pk, seller__user=request.user)
    prop.is_available = False
    prop.save()
    messages.success(request, "Marked as sold!")
    return redirect('seller_dashboard')


# ==================== Reports & Admin ====================

@login_required
@require_POST
def report_issue(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    reason = request.POST.get('reason')
    if reason:
        Report.objects.create(
            report_type='property',
            reported_property=prop,
            reason=reason,
            reported_by=request.user
        )
        messages.success(request, "Report submitted!")
    return redirect('property_detail', pk=pk)


@user_passes_test(lambda u: u.is_superuser)
def view_reports(request):
    reports = Report.objects.all()
    return render(request, 'mainapp/view_reports.html', {'reports': reports})

@login_required
def meeting_request(request, property_id):
    prop = get_object_or_404(Property, pk=property_id)
    seller = prop.seller
    if request.method == "POST":
        message = request.POST.get('message')
        preferred_date = request.POST.get('preferred_date')
        if message:
            MeetingRequest.objects.create(
                buyer=request.user,
                seller=seller,
                property=prop,
                message=message,
                preferred_date=preferred_date or None,
            )
            messages.success(request, "Your meeting request was sent successfully!")
        return redirect('property_detail', pk=property_id)
    return render(request, 'mainapp/meeting_request.html', {'property': prop})


def contact_success(request):
    return render(request, 'mainapp/contact_success.html')



# ==================== Contact Page ====================
def contact_page(request):
    """
    Display a contact page with a simple form allowing visitors
    to send a message or schedule a meeting via email.
    """
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if name and email and message:
            subject = f"New message from {name} via contact page"
            full_message = f"From: {name}\nEmail: {email}\n\nMessage:\n{message}"

            try:
                send_mail(
                    subject,
                    full_message,
                    email,  # Sender's email
                    ['prestigeproperties2030@gmail.com'],  # ✅ Receiver's email
                    fail_silently=False,
                )
                return redirect('contact_success')  # Redirect if sent successfully
            except Exception as e:
                messages.error(request, "Failed to send your message. Please try again later.")
        else:
            messages.error(request, "Please fill all the fields before submitting!")

    return render(request, 'mainapp/contact_page.html')


def subscribe(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if email:
            Subscriber.objects.get_or_create(email=email)
            messages.success(request, "Thanks for subscribing to our mailing list!")
        return redirect('subscribe')
    return render(request, 'mainapp/subscribe.html')
def book_site_visit(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    
    if request.method == 'POST':
        try:
            # Create the booking
            booking = Booking.objects.create(
                property=property_obj,
                buyer=request.user if request.user.is_authenticated else None,
                full_name=request.POST.get('full_name'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                visit_date=request.POST.get('visit_date'),
                visit_time=request.POST.get('visit_time'),
                message=request.POST.get('message', '')
            )
            
            # Redirect to confirmation page
            return redirect('booking_confirmation', pk=booking.id)
            
        except Exception as e:
            messages.error(request, f"Error creating booking: {str(e)}")
            return redirect('property_detail', pk=pk)
    
    # If GET request, show property detail page
    return redirect('property_detail', pk=pk)



def booking_confirmation(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    return render(request, 'mainapp/booking_confirmation.html', {
        'booking': booking,
        'property': booking.property
    })



@login_required
def seller_bookings(request):
    # Get properties owned by the seller
    seller_properties = Property.objects.filter(seller__user=request.user)
    # Get bookings for these properties
    bookings = Booking.objects.filter(property__in=seller_properties).order_by('-visit_date', '-visit_time')
    
    return render(request, 'mainapp/seller_bookings.html', {
        'bookings': bookings
    })

@login_required
@require_POST
def update_booking_status(request, pk):
    booking = get_object_or_404(Booking, pk=pk, property__seller__user=request.user)
    new_status = request.POST.get('status')
    
    if new_status in dict(Booking.STATUS_CHOICES).keys():
        booking.status = new_status
        booking.save()
        messages.success(request, f"Booking status updated to {new_status}.")
    else:
        messages.error(request, "Invalid status.")
    
    return redirect('seller_bookings')