from django.shortcuts import render
from django.db import connection
from .models import RegistrationProfile

def register_view(request):
    recent_registrations = RegistrationProfile.objects.order_by('-registered_at')[:5]
    
    db_name = connection.settings_dict.get('NAME', 'N/A')
    db_user = connection.settings_dict.get('USER', 'N/A')

    context = {
        'recent_registrations': recent_registrations,
        'url_name': 'Register (/register)',
        'current_url': '/register',
        'db_name': db_name,
        'db_user': db_user
    }
    return render(request, 'register/register.html', context)
