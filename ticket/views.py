from django.shortcuts import render
from django.db import connection
from .models import Ticket

def ticket_view(request):
    tickets = Ticket.objects.select_related('show').all().order_by('-purchase_date')
    
    db_name = connection.settings_dict.get('NAME', 'N/A')
    db_user = connection.settings_dict.get('USER', 'N/A')

    # context = {
    #     'tickets': tickets,
    #     'url_name': 'Ticket (/ticket)',
    #     'current_url': '/ticket',
    #     'db_name': db_name,
    #     'db_user': db_user
    # }
    sectors = [
        {
            "name": "Campo VIP",
            "capacity": 100,
            "available": 100,
            "price": 25000,
            "x": 350,
            "y": 500,
            "width": 300,
            "height": 70,
            "color": "gold"
        },
        {
            "name": "Campo Frontal",
            "x": 250,
            "y": 380,
            "width": 500,
            "height": 100,
            "color": "royalblue"
        },
        {
            "name": "Campo Trasero",
            "x": 200,
            "y": 250,
            "width": 600,
            "height": 100,
            "color": "steelblue"
        },
        {
            "name": "Campo VIP",
            "x": 50,
            "y": 250,
            "width": 120,
            "height": 250,
            "color": "crimson"
       },
       {
            "name": "Campo VIP",
            "x": 830,
            "y": 250,
            "width": 120,
            "height": 250,
            "color": "crimson"
        },
        {
            "name": "Campo VIP",
            "x": 250,
            "y": 100,
            "width": 500,
            "height": 100,
            "color": "darkgreen"
            }
    ]
    context = {"sectors": sectors}
    return render(request, 'ticket/ticket.html', context)
