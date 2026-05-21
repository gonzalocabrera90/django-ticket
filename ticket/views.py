from django.shortcuts import render
from django.db import connection
from .models import Ticket

def ticket_view(request):
    tickets = Ticket.objects.select_related('show').all().order_by('-purchase_date')
    
    db_name = connection.settings_dict.get('NAME', 'N/A')
    db_user = connection.settings_dict.get('USER', 'N/A')

    context = {
        'tickets': tickets,
        'url_name': 'Ticket (/ticket)',
        'current_url': '/ticket',
        'db_name': db_name,
        'db_user': db_user
    }
    return render(request, 'url_viewer.html', context)
