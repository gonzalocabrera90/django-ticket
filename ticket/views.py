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

import uuid


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
            
            mensaje = f"¡Pago aprobado con éxito! Tu orden #{orden.id} está confirmada. Se han generado {len(tickets_creados)} tickets."
            clase_alerta = "success"
            
        except Exception as e:
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

# def ticket_view(request):
#     tickets = Ticket.objects.select_related('show').all().order_by('-purchase_date')
    
#     db_name = connection.settings_dict.get('NAME', 'N/A')
#     db_user = connection.settings_dict.get('USER', 'N/A')

#     # context = {
#     #     'tickets': tickets,
#     #     'url_name': 'Ticket (/ticket)',
#     #     'current_url': '/ticket',
#     #     'db_name': db_name,
#     #     'db_user': db_user
#     # }
#     sectors = [
#         {
#             "name": "Campo VIP",
#             "capacity": 100,
#             "available": 100,
#             "price": 25000,
#             "x": 350,
#             "y": 500,
#             "width": 300,
#             "height": 70,
#             "color": "gold"
#         },
#         {
#             "name": "Campo Frontal",
#             "x": 250,
#             "y": 380,
#             "width": 500,
#             "height": 100,
#             "color": "royalblue"
#         },
#         {
#             "name": "Campo Trasero",
#             "x": 200,
#             "y": 250,
#             "width": 600,
#             "height": 100,
#             "color": "steelblue"
#         },
#         {
#             "name": "Campo VIP",
#             "x": 50,
#             "y": 250,
#             "width": 120,
#             "height": 250,
#             "color": "crimson"
#        },
#        {
#             "name": "Campo VIP",
#             "x": 830,
#             "y": 250,
#             "width": 120,
#             "height": 250,
#             "color": "crimson"
#         },
#         {
#             "name": "Campo VIP",
#             "x": 250,
#             "y": 100,
#             "width": 500,
#             "height": 100,
#             "color": "darkgreen"
#             }
#     ]
#     context = {"sectors": sectors}
#     return render(request, 'ticket/ticket.html', context)
