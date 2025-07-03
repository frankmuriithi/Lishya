from django.urls import path
from . import views

urlpatterns = [
    # 🏠 Public Views
    path('', views.index, name='index'),
    path('properties/', views.property_list, name='property_list'),
    path('properties/<int:pk>/', views.property_detail, name='property_detail'),
    path('buyers/', views.buyers, name='buyers'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact_page, name='contact_page'),
    path('subscribe/', views.subscribe, name='subscribe'),



    # ❤️ Favorites & Messages
    path('properties/<int:pk>/favorite/', views.add_to_favorites, name='add_to_favorites'),
    path('favorites/', views.view_favorites, name='view_favorites'),
    path('properties/<int:property_id>/message/', views.send_message, name='send_message'),
    path('properties/<int:property_id>/request-meeting/', views.meeting_request, name='meeting_request'),


    # ✍️ Authentication
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # 🧑‍💼 Seller Views
    path('seller/dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('seller/properties/create/', views.create_property, name='create_property'),
    path('seller/properties/<int:pk>/edit/', views.edit_property, name='edit_property'),
    path('seller/properties/<int:pk>/sold/', views.mark_as_sold, name='mark_as_sold'),

    # ⚠️ Reports & Admin
    path('properties/<int:pk>/report/', views.report_issue, name='report_issue'),
    path('admin/reports/', views.view_reports, name='view_reports'),

    #booking 
     path('properties/<int:pk>/book-site-visit/', views.
     
    book_site_visit, name='book_site_visit'),

    # 🗓️ Booking Confirmation
path('properties/<int:pk>/book-site-visit/', views.book_site_visit, name='book_site_visit'),
]
