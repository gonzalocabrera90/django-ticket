from django.urls import path
from . import views

urlpatterns = [
    path('shows/', views.shows_view, name='shows'),
    path('buscar/', views.buscar_shows, name='buscar_shows'),
    # Ruta dinámica que acepta el ID numérico del lugar
    path('shows/<int:place_id>/mapa/', views.mapa_espectaculo_view, name='mapa_espectaculo'),
    path('show/<int:show_id>/mapa/', views.detalle_mapa_show, name='espectaculo'),
]
