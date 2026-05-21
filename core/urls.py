from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('home/', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('shows/', views.shows_view, name='shows'),
    path('ticket/', views.ticket_view, name='ticket'),
]
