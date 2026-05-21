from django.shortcuts import render
from django.db import connection
from .models import Show

def shows_view(request):
    shows = Show.objects.all().order_by('date')
    
    db_name = connection.settings_dict.get('NAME', 'N/A')
    db_user = connection.settings_dict.get('USER', 'N/A')

    context = {
        'shows': shows,
        'url_name': 'Shows (/shows)',
        'current_url': '/shows',
        'db_name': db_name,
        'db_user': db_user
    }
    return render(request, 'shows/shows.html', context)
