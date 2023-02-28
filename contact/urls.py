from django.urls import path
from contact.views import *

urlpatterns = [
    path('getintouch', ContactView.as_view(), name="Contacted Us"),
    path('redirect', subredirect, name="Redirect"),
    path('confirm', confirm, name="Booking Confirm"),
]