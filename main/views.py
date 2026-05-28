from django.shortcuts import render
from django.db import connection
from .models import MainDashboard
from shows.models import Show
from register.models import User
from ticket.models import Ticket

def index_view(request):
    dashboard = Show.objects.all()
    print(dashboard)
    if not dashboard:
        dashboard = MainDashboard(
            title="DjangoTicket Portal",
            welcome_message="Bienvenido al portal central de DjangoTicket. La plataforma está totalmente integrada y conectada a PostgreSQL local."
        )
    
    # Query database stats to show DB connectivity
    stats = {
        'total_shows': Show.objects.count(),
        'total_users': User.objects.count(),
        'total_tickets': Ticket.objects.count(),
    }
    
    db_name = connection.settings_dict.get('NAME', 'N/A')
    db_user = connection.settings_dict.get('USER', 'N/A')

    context = {
        'dashboard': dashboard,
        'stats': stats,
        'url_name': 'Ruta Raíz (/)',
        'current_url': '/',
        'db_name': db_name,
        'db_user': db_user
    }
    return render(request, 'main/main.html', context)
