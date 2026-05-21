from django.urls import path
from . import views

urlpatterns = [
    path('shows/', views.shows_view, name='shows'),
]
