from django.contrib.auth import get_user_model
from shows.models import Event, Show, ShowSector # Usá tus imports reales

User = get_user_model()

# 1. Buscamos el superusuario que acabás de crear (traemos el primero que encuentre)
admin_user = User.objects.filter(is_superuser=True).first()

# 2. Buscamos tu evento de prueba (por ejemplo, el de Coldplay)
# Si no tenés ninguno creado, el admin_user puede ir al panel web a crearlo.
evento = Event.objects.first()

if evento and admin_user:
    evento.organizador = admin_user
    evento.save()
    print(f"✅ Éxito: El evento '{evento.title}' ahora le pertenece a {admin_user.email}")
else:
    print("⚠️ Asegurate de tener al menos un Evento creado en la base de datos.")