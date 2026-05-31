from django.shortcuts import render, get_object_or_404
from django.db import connection
from django.db.models import Q
from .models import ShowPlace, Show, ShowSector, MapLayoutObject, Category, Event

# def shows_view(request):
#     """Muestra la pantalla de inicio limpia con los eventos destacados y categorías"""
#     categorias = Category.objects.all()
    
#     # Traemos los eventos (no los shows) que tengan al menos una función planificada
#     # Optimizamos trayendo la categoría de un solo viaje
#     eventos_destacados = Event.objects.select_related('category').filter(
#         shows__isnull=False
#     ).distinct()[:6]
    
#     return render(request, 'shows/shows.html', {
#         'categorias': categorias,
#         'events': eventos_destacados # Cambiamos 'shows' por 'events' para el template
#     })
def shows_view(request, event_id):
    # Traemos el evento o tiramos 404
    evento = get_object_or_404(Event, id=event_id)
    print("evento")
    print(evento)
    # Obtenemos todos los shows asociados a este evento ordenados por fecha
    shows = Show.objects.filter(event=evento).order_by('date')
    
    # Buscamos el precio mínimo sugerido para mostrar un "Desde $X"
    precio_minimo = None
    if shows.exists():
        precio_minimo = min([show.price for show in shows])

    return render(request, 'shows/shows.html', {
        'evento': evento,
        'shows': shows,
        'precio_minimo': precio_minimo
    })
# def shows_view(request):
#     shows = Show.objects.all().order_by('date')
    
#     db_name = connection.settings_dict.get('NAME', 'N/A')
#     db_user = connection.settings_dict.get('USER', 'N/A')

#     context = {
#         'shows': shows,
#         'url_name': 'Shows (/shows)',
#         'current_url': '/shows',
#         'db_name': db_name,
#         'db_user': db_user
#     }
#     return render(request, 'shows/shows.html', context)

#     """Muestra la pantalla de inicio limpia con los eventos destacados y categorías"""
#     categorias = Category.objects.all()
    
#     # Traemos los eventos (no los shows) que tengan al menos una función planificada
#     # Optimizamos trayendo la categoría de un solo viaje
#     eventos_destacados = Event.objects.select_related('category').filter(
#         shows__isnull=False
#     ).distinct()[:6]
    
#     return render(request, 'shows/index.html', {
#         'categorias': categorias,
#         'events': eventos_destacados # Cambiamos 'shows' por 'events' para el template
#     })

def buscar_shows(request):
    """Vista exclusiva para procesar y renderizar los resultados de búsqueda"""
    categorias = Category.objects.all()
    
    # Capturamos los parámetros del formulario GET
    query_texto = request.GET.get('q', '').strip()
    query_categoria = request.GET.get('category', '').strip()
    
    # IMPORTANTE: Eliminamos 'place' del select_related porque no existe en Show.
    # Usamos distinct() al final para evitar que si un show tiene 5 sectores, 
    # aparezca 5 veces repetido en los resultados de búsqueda.
    #resultados = Show.objects.select_related('category').order_by('date').distinct()
    resultados = Event.objects.select_related('category').filter(shows__isnull=False).distinct()
    # Aplicamos filtros si el usuario ingresó datos
    if query_texto:
        resultados = resultados.filter(
            Q(title__icontains=query_texto) |
            Q(description__icontains=query_texto) |
            # Buscamos de forma segura si el nombre del estadio coincide con alguna de sus funciones
            Q(shows__place__name__icontains=query_texto) |
            Q(shows__place__address__city__icontains=query_texto)
        ).distinct()
        
    if query_categoria:
        resultados = resultados.filter(category__slug=query_categoria)

    return render(request, 'shows/resultados_busqueda.html', {
        'events': resultados,
        'categorias': categorias,
        'query_texto': query_texto,
        'query_categoria': query_categoria,
    })

# def mapa_espectaculo_view(request, place_id):
#     # Buscamos el lugar por su ID trayendo de forma eficiente sus sectores relacionados
#     place = get_object_or_404(
#         ShowPlace.objects.prefetch_related('sectors'), 
#         id=place_id
#     )
    
#     # Pasamos el objeto 'place' al contexto. 
#     # Desde el template accederemos a los sectores con 'place.sectors.all'
#     return render(request, 'shows/mapa_espectaculo.html', {
#         'place': place
#     })

# def detalle_mapa_show(request, show_id):
#     # """Renderiza el mapa interactivo para una FECHA/FUNCIÓN específica"""
#     # # 1. Buscamos el show (función) que quiere ver el usuario, trayendo su evento y estadio asociados
#     # show = get_object_or_404(Show.objects.select_related('event', 'place'), id=show_id)
    
#     # # 2. El lugar (estadio) ahora viene directo del modelo Show, ¡mucho más limpio!
#     # place = show.place
    
#     # # 3. Traemos los precios e inventarios comerciales de ESTE show específico (esta noche)
#     # show_sectors = ShowSector.objects.filter(show=show).select_related('sector')
    
#     # # 4. Traemos la infraestructura fija de ese estadio
#     # layout_objects = MapLayoutObject.objects.filter(place=place)

#     # return render(request, 'shows/detalle_show.html', {
#     #     'show': show,
#     #     'place': place,
#     #     'show_sectors': show_sectors,
#     #     'layout_objects': layout_objects
#     # })
#     # CÓMO DEBERÍA VERSE TU VISTA DEL MAPA

#     # 1. Buscamos la función específica por su ID único
#     show = get_object_or_404(Show, id=show_id)
    
#     # 2. A partir de ESA función, extraemos el estadio correcto y sus sectores
#     estadio = show.place 
#     sectores_del_estadio = estadio.sectors.all()
    
#     # 3. Traemos los precios y disponibilidad reales de ESA noche
#     show_sectores = show.showsector_set.all() # O ShowSector.objects.filter(show=show)

#     return render(request, 'shows/detalle_show.html', {
#         'show': show,
#         'estadio': estadio,
#         'show_sectores': show_sectores
#     })

# CÓMO DEBERÍA VERSE TU VISTA DEL MAPA
def vista_del_mapa(request, show_id):
    # 1. Buscamos la función específica por su ID único
    show = get_object_or_404(Show, id=show_id)
    # show = get_object_or_404(Show.objects.select_related('event', 'place'), id=show_id)
    
#     # # 2. El lugar (estadio) ahora viene directo del modelo Show, ¡mucho más limpio!
#     # place = show.place
    # 2. A partir de ESA función, extraemos el estadio correcto y sus sectores
    estadio = show.place 
    sectores_del_estadio = estadio.sectors.all()
    
    # 3. Traemos los precios y disponibilidad reales de ESA noche
    # show_sectores = show.showsector_set.all() # O ShowSector.objects.filter(show=show)
    # show_sectores = show.show_sectors.all()
    show_sectores = ShowSector.objects.filter(show=show)
    layout_objects = MapLayoutObject.objects.filter(place=estadio)
    fecha_formateada = show.date.strftime("%Y-%m-%d %H:%M")
    print(layout_objects[0].name )
    return render(request, 'shows/detalle_show.html', {
        'show': show,
        'place': estadio,
        'show_sectors': show_sectores,
        'layout_objects': layout_objects,
        'fecha_formateada': fecha_formateada
    })
