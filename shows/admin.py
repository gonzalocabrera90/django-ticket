from django.contrib import admin
from .models import ShowPlace, Sector, MapLayoutObject, Category, Event, Show, ShowSector

# admin.site.register(ShowPlace)
# admin.site.register(Sector)
# admin.site.register(MapLayoutObject)
# admin.site.register(Category)
# admin.site.register(Event)
# admin.site.register(Show)
# admin.site.register(ShowSector)


# 1. Mantenemos los registros simples para los modelos de infraestructura física
admin.site.register(ShowPlace)
admin.site.register(Sector)
admin.site.register(MapLayoutObject)
admin.site.register(ShowSector)

# 2. Personalizamos la visualización de los modelos comerciales

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'color_hex') # Podés ver el nombre y el color asignado en columnas

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    # Esto te permite ver en el listado general qué banda pertenece a qué Organizador
    list_display = ('title', 'category', 'organizador')
    # Agrega filtros laterales en el Admin para buscar rápido por empresa o género musical
    list_filter = ('category', 'organizador')
    # Habilita un buscador por texto para el nombre de la banda
    search_fields = ('title',)

@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    # Te permite ver de un vistazo el evento, el estadio, la fecha exacta y el precio base
    list_display = ('event', 'place', 'date', 'price')
    list_filter = ('date', 'place')