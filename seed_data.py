import os
import django
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticket_project.settings')
django.setup()

from main.models import MainDashboard
from home.models import HomeBanner
from login.models import LoginLog
from register.models import RegistrationProfile
from shows.models import Show
from ticket.models import Ticket

def seed():
    print("Seeding database...")
    
    # 1. Main Dashboard
    MainDashboard.objects.all().delete()
    dashboard = MainDashboard.objects.create(
        title="DjangoTicket Portal Principal",
        welcome_message="¡Conexión establecida con éxito! Los datos que ves en esta pantalla y en el resto de las rutas son dinámicos y provienen de las tablas de tu base de datos PostgreSQL local, administradas individualmente por cada una de las 6 aplicaciones."
    )
    print("Created MainDashboard")

    # 2. Home Banners
    HomeBanner.objects.all().delete()
    HomeBanner.objects.create(title="Gran Concierto de Invierno", subtitle="Disfruta de la mejor filarmónica el próximo mes con un 20% de descuento.")
    HomeBanner.objects.create(title="Festival de Teatro Independiente", subtitle="15 obras locales en escena durante toda la semana.")
    HomeBanner.objects.create(title="¡Nuevas funciones de Stand-Up!", subtitle="Risas aseguradas todos los viernes por la noche.")
    print("Created HomeBanners")

    # 3. Login Log
    LoginLog.objects.all().delete()
    LoginLog.objects.create(username="gcuser", success=True, ip_address="127.0.0.1")
    LoginLog.objects.create(username="admin", success=True, ip_address="192.168.1.10")
    LoginLog.objects.create(username="usuario_test", success=False, ip_address="127.0.0.1")
    LoginLog.objects.create(username="gcuser", success=True, ip_address="127.0.0.1")
    print("Created LoginLogs")

    # 4. Registration Profiles
    RegistrationProfile.objects.all().delete()
    RegistrationProfile.objects.create(username="juan_perez", email="juan@example.com", newsletter_opt_in=True)
    RegistrationProfile.objects.create(username="maria_gomez", email="maria@example.com", newsletter_opt_in=False)
    RegistrationProfile.objects.create(username="carlos_ruiz", email="carlos@example.com", newsletter_opt_in=True)
    print("Created RegistrationProfiles")

    # 5. Shows
    Show.objects.all().delete()
    s1 = Show.objects.create(
        title="Coldplay - Music of the Spheres",
        description="El regreso de Coldplay a los escenarios en una noche mágica llena de luces, pulseras interactivas y grandes éxitos.",
        date=timezone.now() + timedelta(days=30),
        price=150.00
    )
    s2 = Show.objects.create(
        title="La Traviata - Ópera Metropolitana",
        description="La aclamada producción de Verdi interpretada por los solistas más destacados del panorama internacional.",
        date=timezone.now() + timedelta(days=15),
        price=95.50
    )
    s3 = Show.objects.create(
        title="Stand Up Comedy: Noche de Risas",
        description="Un show imperdible con tres comediantes invitados que te harán reír de principio a fin.",
        date=timezone.now() + timedelta(days=5),
        price=25.00
    )
    print("Created Shows")

    # 6. Tickets
    Ticket.objects.all().delete()
    Ticket.objects.create(show=s1, buyer_name="Juan Perez", buyer_email="juan@example.com", seat_number="A-24")
    Ticket.objects.create(show=s1, buyer_name="Maria Gomez", buyer_email="maria@example.com", seat_number="A-25")
    Ticket.objects.create(show=s2, buyer_name="Carlos Ruiz", buyer_email="carlos@example.com", seat_number="B-12")
    print("Created Tickets")
    
    print("Seeding completed successfully!")

if __name__ == '__main__':
    seed()
