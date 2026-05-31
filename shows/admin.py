from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import ShowPlace, Sector, MapLayoutObject, Category, Event, Show, ShowSector

admin.site.register(ShowPlace)
admin.site.register(Sector)
admin.site.register(MapLayoutObject)
admin.site.register(Category)
admin.site.register(Event)
admin.site.register(Show)
admin.site.register(ShowSector)
