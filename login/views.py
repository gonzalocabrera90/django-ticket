from django.shortcuts import render
from django.db import connection
from .models import LoginLog

def login_view(request):
    recent_logins = LoginLog.objects.order_by('-timestamp')[:5]
    
    db_name = connection.settings_dict.get('NAME', 'N/A')
    db_user = connection.settings_dict.get('USER', 'N/A')

    context = {
        'recent_logins': recent_logins,
        'url_name': 'Login (/login)',
        'current_url': '/login',
        'db_name': db_name,
        'db_user': db_user
    }
    return render(request, 'login/login.html', context)
