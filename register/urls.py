from django.urls import path
from .views import (
    register_view,
    address_register_view,
    email_verification_sent,
    activate,
    load_regions,
    load_cities,
    activate_account_view,
)

urlpatterns = [
    path(
        'register/',
        register_view,
        name='register'
    ),
    path(
        'register/address/',
        address_register_view,
        name='address-register'
    ),
    path(
        'activate/<uidb64>/<token>/',
        activate_account_view,
        name='activate-account'
    ),
    path(
        'email-sent/',
        email_verification_sent,
        name='email-verification-sent'
    ),
    path(
        'activate/<uidb64>/<token>/',
        activate,
        name='activate'
    ),
    path(
        'register/ajax/load-regions/',
        load_regions,
        name='ajax-load-regions'
    ),
    path(
        'register/ajax/load-cities/',
        load_cities,
        name='ajax-load-cities'
    ),
]