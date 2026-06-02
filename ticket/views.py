from django.shortcuts import render
from django.db import connection
from .models import Ticket, Order

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from shows.models import ShowSector

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
