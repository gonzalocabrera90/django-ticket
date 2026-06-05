from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Order

def enviar_correo_confirmacion(orden: Order):
    """
    Genera un correo basado en un template HTML con los detalles de la compra
    y los códigos de los tickets, y lo despacha al usuario.
    """
    # 1. Definimos el asunto y los datos que irán al diseño
    asunto = f"🎟️ ¡Tu compra para {orden.show.event.title} fue confirmada! - Orden #{orden.id}"
    contexto = {
        'orden': orden,
        'tickets': orden.tickets.all()
    }
    
    # 2. Renderizamos el diseño HTML del correo
    html_message = render_to_string('ticket/emails/confirmacion_compra.html', contexto)
    
    # 3. Creamos una versión en texto plano para clientes de correo viejos
    plain_message = strip_tags(html_message)
    
    # 4. Despachamos el email
    send_mail(
        subject=asunto,
        message=plain_message,
        from_email=None,  # Usa el DEFAULT_FROM_EMAIL de settings
        recipient_list=[orden.user.email],
        html_message=html_message,
        fail_silently=False,
    )
