from django.shortcuts import render
from django.db import connection
from .models import HomeBanner

def home_view(request):
    banners = HomeBanner.objects.filter(active=True)
    
    db_name = connection.settings_dict.get('NAME', 'N/A')
    db_user = connection.settings_dict.get('USER', 'N/A')

    context = {
        'banners': banners,
        'url_name': 'Home (/home)',
        'current_url': '/home',
        'db_name': db_name,
        'db_user': db_user
    }
    return render(request, 'url_viewer.html', context)
