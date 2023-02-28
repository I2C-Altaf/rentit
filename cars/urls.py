from django.urls import path
from cars.views import *

urlpatterns = [
    # path('cars/', CarsView.as_view(), name='Find Car'),
    path('cars/all/', allcars, name='All Cars'),
    path('cars/<int:pk>', carlist, name='Detailed Car'),
    path('cars/popular/', PopularCarView.as_view(), name='Popular Cars'),
    
    path('home/', home, name='Home'),
    path('about/', about, name='About Us'),
    path('faqs/', faq, name='FAQs'),
    
    ################## STRIPE ###########################
    path('create-checkout-session/', create_checkout_session, name='checkout'),
    path('success/', success,name='success'),
    path('cancel/<int:pk>/', cancel,name='cancel'),
    path('webhooks/stripe/', webhook,name='webhook'),
    path('auto/', auto, name='auto' ),
    path('mybook/', mybook, name='My Bookings'),
    path('mybook/cancel/', canclebooking, name='Cancel Booking'),
    path('contactus/', contact, name='Contact Us'),
]