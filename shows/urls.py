from django.urls import path
from . import views

urlpatterns = [
    #path('shows/', views.shows_view, name='shows'),
    # Ruta dinámica que acepta el ID numérico del lugar
    #path('shows/<int:place_id>/mapa/', views.mapa_espectaculo_view, name='mapa_espectaculo'),
    #path('show/<int:show_id>/mapa/', views.detalle_mapa_show, name='detalle_mapa_show'),
    path('shows/<int:event_id>/', views.shows_view, name='shows'), # detalles del evento para elegir fecha
    path('buscar/', views.buscar_shows, name='buscar_shows'), # vista de busqueda
    path('show/<int:show_id>/mapa/', views.vista_del_mapa, name='ver_mapa'), # mostrar el mapa del estadio para fecha
]
# en el detalle fijar redireccion, y en este ultimo path mostrar el mapa