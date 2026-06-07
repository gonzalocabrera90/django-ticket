from django.shortcuts import render, get_object_or_404, redirect
from django.db import connection
from .models import Ticket, Order
from .payment_processors import get_payment_processor
from shows.models import ShowSector

from django.db import transaction
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.urls import reverse

from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

import uuid

from .utils import enviar_correo_confirmacion

@login_required
def iniciar_reserva(request):
    if request.method == "POST":
        # 1. Obtenemos los datos que envía el mapa interactivo
        sector_id = request.POST.get('show_sector_id')
        cantidad = int(request.POST.get('quantity', 1))
        
        # 2. Abrimos un bloque atómico seguro para congelar la fila de la BD
        try:
            with transaction.atomic():
                # select_for_update() bloquea este ShowSector específico en la BD 
                # hasta que termine esta función. Nadie más puede leer/modificar sus asientos.
                show_sector = ShowSector.objects.select_for_update().get(id=sector_id)
                
                # 3. Validamos stock disponible
                if show_sector.available < cantidad:
                    return JsonResponse({'status': 'error', 'message': 'Ya no quedan asientos suficientes en este sector.'}, status=400)
                
                # 4. Restamos temporalmente el inventario
                show_sector.available -= cantidad
                show_sector.save()
                
                # 5. Calculamos el total monetario
                total = show_sector.price * cantidad
                
                # 6. Creamos la orden en modo PENDING
                nueva_orden = Order.objects.create(
                    user=request.user,
                    show=show_sector.show,
                    show_sector=show_sector,
                    quantity=cantidad,
                    total_price=total,
                    status='PENDING'
                )
                
            # Al salir del bloque transaction.atomic(), Django libera el bloqueo en la BD
            return JsonResponse({
                'status': 'success',
                'message': 'Reserva temporal exitosa. Tienes 10 minutos para pagar.',
                'order_id': nueva_orden.id
            })
            
        except ShowSector.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Sector no encontrado.'}, status=404)
            
    return JsonResponse({'status': 'error', 'message': 'Método no permitido.'}, status=405)

def mock_checkout_view(request, order_id):
    """Muestra la pantalla simulada de la pasarela de pagos"""
    orden = get_object_or_404(Order, id=order_id, status='PENDING')
    return_url = request.GET.get('return_url', '/')
    
    context = {
        'orden': orden,
        'return_url': return_url
    }
    return render(request, 'ticket/mock_checkout.html', context)


def payment_feedback_view(request):
    """
    Recibe la respuesta de la pasarela (simulando un Webhook/Redirect).
    Modifica la base de datos según el resultado del pago.
    """
    procesador = get_payment_processor()
    
    # El procesador analiza el request y nos devuelve un diccionario estandarizado
    resultado = procesador.verify_webhook(request)
    
    order_id = resultado.get('order_id')
    if not order_id:
        return HttpResponseBadRequest("Falta el ID de la orden.")
        
    orden = get_object_or_404(Order, id=order_id)

    if resultado['success']:
    #     # ¡El pago fue exitoso! Confirmamos la orden
    #     orden.status = 'PAID'
    #     orden.save()
        
    #     # Opcional: Acá es donde en el futuro generarás los Tickets físicos
    #     mensaje = f"¡Pago aprobado con éxito! Tu orden #{orden.id} está confirmada."
    #     clase_alerta = "success"
    # Usamos una transacción atómica para asegurarnos de que se guarde la orden
        # Y se creen TODOS los tickets correspondientes. Si uno falla, no se guarda nada.
        try:
            with transaction.atomic():
                # 1. Cambiamos el estado de la orden
                orden.status = 'PAID'
                orden.save()
                
                # 2. Generamos los tickets físicos según la cantidad comprada
                tickets_creados = []
                for _ in range(orden.quantity):
                    ticket = Ticket.objects.create(
                        order=orden,
                        show_sector=orden.show_sector  # <-- Agregamos esto para cumplir con tu modelo
                    )
                    tickets_creados.append(ticket)

                    # with transaction.atomic():
                    #     # ... (guardado de orden y creación de tickets)
                    #     pass
                    
                    # Fuera del bloque atómico pero dentro del if success, gatillamos el email
            print("Gatillando función de email...") # Meté este print de control
            enviar_correo_confirmacion(orden)
            print("¡Función de email ejecutada con éxito!")        
            mensaje = f"¡Pago aprobado con éxito! Tu orden #{orden.id} está confirmada. Se han generado {len(tickets_creados)} tickets y se envió un mail de confirmación."
            clase_alerta = "success"
            
        except Exception as e:
            # IMPRESCINDIBLE: Esto nos va a decir en la consola qué está fallando por dentro
            print("\n❌ ❌ ❌ ¡¡¡EL PROCESO DE EMAIL ACABA DE FALLAR!!! ❌ ❌ ❌")
            print(f"Error real detectado: {str(e)}")
            import traceback
            traceback.print_exc() # Esto te pinta el número de línea exacto del error
            print("❌ ❌ ❌ ------------------------------------------- ❌ ❌ ❌\n")
            
            mensaje = f"El pago fue aprobado, pero ocurrió un error al generar tus tickets: {str(e)}. Por favor, contacta a soporte."
            clase_alerta = "warning"
    else:
        # El pago falló o fue cancelado. Expiramos/Cancelamos la orden
        orden.status = 'EXPIRED'  # O 'REFUNDED' / 'REJECTED' según prefieras
        orden.save()
        mensaje = f"El pago de la orden #{orden.id} fue rechazado o cancelado. Los asientos fueron liberados."
        clase_alerta = "danger"
        
    return render(request, 'ticket/payment_feedback.html', {
        'mensaje': mensaje,
        'clase_alerta': clase_alerta,
        'orden': orden
    })




@login_required
@require_POST
def iniciar_pago_view(request):
    """
    Recibe la selección del mapa interactivo, crea la orden PENDING
    y redirige al usuario a la pasarela de pago correspondiente.
    """
    show_sector_id = request.POST.get('show_sector_id')
    cantidad = int(request.POST.get('quantity', 1))
    
    # 1. Traemos el sector del show
    show_sector = get_object_or_404(ShowSector, id=show_sector_id)
    
    # 2. Validamos que haya stock suficiente antes de hacer nada
    if show_sector.available < cantidad:
        return render(request, 'ticket/payment_feedback.html', {
            'mensaje': "Lo sentimos, ya no quedan suficientes asientos disponibles en este sector.",
            'clase_alerta': "danger"
        })
        
    # 3. Creamos la orden en estado PENDING
    # Nota: Como tu @property 'available' ahora resta las órdenes PENDING,
    # al ejecutarse esta línea, el stock baja automáticamente para el resto del mundo.
    orden = Order.objects.create(
        user=request.user,
        show=show_sector.show,
        show_sector=show_sector,
        quantity=cantidad,
        total_price=show_sector.price * cantidad,
        status='PENDING'
    )
    
    # 4. Usamos nuestro Patrón Strategy para obtener el procesador activo
    procesador = get_payment_processor()
    
    # Definimos a dónde tiene que volver el usuario de forma absoluta tras el pago
    url_retorno = request.build_absolute_uri(reverse('ticket:payment_feedback'))
    
    # 5. Generamos el link de pago (que en este caso irá a nuestro Mock Checkout)
    link_de_pago = procesador.generate_payment_link(orden, return_url=url_retorno)
    
    # ¡Redirigimos al usuario a la pasarela!
    return redirect(link_de_pago)


@csrf_exempt  # Desactivamos CSRF temporalmente para facilitar que aplicaciones externas le peguen al endpoint
@require_POST
def validar_ticket_api(request):
    """
    Endpoint de API para los molinetes del estadio.
    Recibe el UUID del ticket, valida su estado y registra el ingreso.
    """
    import json
    
    try:
        data = json.loads(request.body)
        ticket_code = data.get('ticket_code')
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'JSON inválido.'}, status=400)
        
    if not ticket_code:
        return JsonResponse({'status': 'error', 'message': 'Falta el código del ticket.'}, status=400)
        
    try:
        # Buscamos el ticket por su UUID único
        #ticket = Ticket.objects.get(ticket_code=ticket_code)

        # Mejorames el .get. Buscamos el ticket y pre-cargamos de un solo golpe toda la cadena de relaciones
        ticket = Ticket.objects.select_related(
            'show_sector__show__event',  # Junta Ticket -> ShowSector -> Show -> Event
            'show_sector__sector',      # Junta Ticket -> ShowSector -> Sector (para el nombre del sector)
            'order__user'               # Junta Ticket -> Order -> User (para el nombre del comprador)
        ).get(ticket_code=ticket_code)
                
        # Caso 1: El ticket ya fue escaneado antes (¡ALERTA DE FRAUDE!)
        if ticket.is_used:
            return JsonResponse({
                'status': 'RECHAZADO',
                'message': f'¡ALERTA! Este ticket ya ingresó el {ticket.used_at.strftime("%d/%m/%Y a las %H:%M")} hs.',
                'evento': ticket.show_sector.show.event.title,
                'sector': ticket.show_sector.sector.name
            }, status=409) # Conflict
            
        # Caso 2: El ticket es válido y está listo para usar
        ticket.is_used = True
        ticket.used_at = timezone.now()
        ticket.save()
        
        return JsonResponse({
            'status': 'OK',
            'message': '¡ACCESO CONCEDIDO! Bienvenido al estadio.',
            'evento': ticket.show_sector.show.event.title,
            'sector': ticket.show_sector.sector.name,
            'comprador': ticket.order.user.get_full_name() or ticket.order.user.username
        }, status=200)
        
    except Ticket.DoesNotExist:
        # Caso 3: El código es inventado o falso
        return JsonResponse({
            'status': 'RECHAZADO',
            'message': 'ERROR: El ticket no existe en el sistema. Código falso.'
        }, status=404)

def panel_control_accesos_view(request):
    """Muestra la interfaz web interactiva para simular el escáner del staff"""
    return render(request, 'ticket/scanner_simulador.html')

@login_required(login_url='login') # <-- Protegemos la vista
def my_tickets_view(request):
    # Tu query excelente se mantiene idéntica
    ordenes = Order.objects.filter(
        user=request.user, 
        status='PAID'
    ).select_related(
        'show__event', 
        'show__place', 
        'show_sector__sector'
    ).prefetch_related('tickets').order_by('-id')
    
    return render(request, 'ticket/my-tickets.html', {'ordenes': ordenes})
