from django.urls import path
from .views import login_view, verify_login_code_view, logout_view

urlpatterns = [
    #path('login/', views.login_view, name='login'),
    path(
        'login/',
        login_view,
        name='login'
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
