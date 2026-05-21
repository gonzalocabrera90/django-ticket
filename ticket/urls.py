from django.urls import path
from . import views

urlpatterns = [
    path('ticket/', views.ticket_view, name='ticket'),
]
