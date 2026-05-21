from django.shortcuts import render
from django.db import connection

def get_db_context():
    try:
        # Try to ensure database connection is active
        connection.ensure_connection()
        db_name = connection.settings_dict.get('NAME', 'N/A')
        db_user = connection.settings_dict.get('USER', 'N/A')
    except Exception as e:
        db_name = "Sin conexión"
        db_user = "gcuser (Configurado)"
    return {
        'db_name': db_name,
        'db_user': db_user
    }

def index_view(request):
    context = get_db_context()
    context.update({
        'url_name': 'Ruta Raíz (/)',
        'current_url': '/'
    })
    return render(request, 'url_viewer.html', context)

def home_view(request):
    context = get_db_context()
    context.update({
        'url_name': 'Home (/home)',
        'current_url': '/home'
    })
    return render(request, 'url_viewer.html', context)

def login_view(request):
    context = get_db_context()
    context.update({
        'url_name': 'Login (/login)',
        'current_url': '/login'
    })
    return render(request, 'url_viewer.html', context)

def register_view(request):
    context = get_db_context()
    context.update({
        'url_name': 'Register (/register)',
        'current_url': '/register'
    })
    return render(request, 'url_viewer.html', context)

def shows_view(request):
    context = get_db_context()
    context.update({
        'url_name': 'Shows (/shows)',
        'current_url': '/shows'
    })
    return render(request, 'url_viewer.html', context)

def ticket_view(request):
    context = get_db_context()
    context.update({
        'url_name': 'Ticket (/ticket)',
        'current_url': '/ticket'
    })
    return render(request, 'url_viewer.html', context)
