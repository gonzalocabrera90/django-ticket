from django.urls import path
from .views import login_view, account_not_verified_view, resend_activation_email_view, verify_login_code_view, logout_view

urlpatterns = [
    #path('login/', views.login_view, name='login'),
    path(
        'login/',
        login_view,
        name='login'
    ),
    path(
        'account-not-verified/',
        account_not_verified_view,
        name='account-not-verified'
    ),
    path(
        'resend-activation-email/',
        resend_activation_email_view,
        name='resend-activation-email'
    ),
    path(
        'verify-login/',
        verify_login_code_view,
        name='verify-login'
    ),
    path(
        'logout/',
        logout_view,
        name='logout'
    ),
]
