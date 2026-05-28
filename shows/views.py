from django.shortcuts import render
from django.db import connection

from django.shortcuts import render, get_object_or_404
from .models import ShowPlace, Show, ShowSector, MapLayoutObject

def shows_view(request):
    shows = Show.objects.all().order_by('date')
    
    db_name = connection.settings_dict.get('NAME', 'N/A')
    db_user = connection.settings_dict.get('USER', 'N/A')

    context = {
        'shows': shows,
        'url_name': 'Shows (/shows)',
        'current_url': '/shows',
        'db_name': db_name,
        'db_user': db_user
    }
    return render(request, 'shows/shows.html', context)


def mapa_espectaculo_view(request, place_id):
    # Buscamos el lugar por su ID trayendo de forma eficiente sus sectores relacionados
    place = get_object_or_404(
        ShowPlace.objects.prefetch_related('sectors'), 
        id=place_id
    )
    
    # Pasamos el objeto 'place' al contexto. 
    # Desde el template accederemos a los sectores con 'place.sectors.all'
    return render(request, 'shows/mapa_espectaculo.html', {
        'place': place
    })
from django.shortcuts import render, get_object_or_404
from .models import Show, ShowSector, MapLayoutObject, ShowPlace

def detalle_mapa_show(request, show_id):
    # 1. Traemos el Show
    show = get_object_or_404(Show, id=show_id)
    
    # 2. Traemos los ShowSectors vinculados
    show_sectors = ShowSector.objects.filter(show=show).select_related('sector__place')
    
    # --- CONTROL DE SEGURIDAD EN LA TERMINAL ---
    print("====== DEBUGGING DETALLE MAPA SHOW ======")
    print(f"Buscando Show: {show.title} (ID: {show.id})")
    print(f"Cantidad de ShowSectors encontrados para este show: {show_sectors.count()}")
    
    # 3. Obtenemos el lugar físico de forma segura garantizando que no sea None si hay sectores
    if show_sectors.exists():
        place = show_sectors.first().sector.place
        print(f"Estadio encontrado con éxito: {place.name} (ID: {place.id})")
    else:
        place = None
        print("❌ ALERTA: 'place' es None porque este Show no tiene ningún ShowSector asociado en la DB.")
    print("=========================================")

    # 4. Traemos la infraestructura
    layout_objects = MapLayoutObject.objects.filter(place=place) if place else []

    return render(request, 'shows/detalle_show.html', {
        'show': show,
        'place': place,
        'show_sectors': show_sectors,
        'layout_objects': layout_objects
    })