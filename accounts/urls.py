from django.urls import path
from accounts.views import *

urlpatterns = [
    path('accounts/register/', signup, name='auth_register'),
    # path('accounts/edit/', ProfileView.as_view(), name='edit_profile'),
    # path('accounts/delete', ProfileView.as_view(), name='Delete Account'),
    path('accounts/login/', login, name='token_obtain_pair'),
   
    path('otp/', OtpView.as_view(), name='generate_otp'),
    path('verifyotp/', OtpVerifyView.as_view(), name='generate_otp'),
    path('forgot/', ForgotPasswordView.as_view(), name='forgot_password'),

    path('cards/add',CardView.as_view(), name='add_card'),
    path('cards/show', CardView.as_view(), name='Show Cards'),
    path('cards/update', CardView.as_view(), name='Show Cards'),
    path('cards/delete', CardView.as_view(), name="Delete Card"),

    path('subscribe', subscribe, name="Subscribe"),
    path('accounts/logout', lout, name='logout'),
]