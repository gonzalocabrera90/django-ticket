from django.db import models
from django.core.exceptions import ValidationError

class ShowPlace(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre del Lugar")
    capacity = models.PositiveIntegerField(verbose_name="Capacidad Total del Lugar")
    # Definimos el viewBox del mapa para que el SVG sepa cómo escalar (ej: "0 0 1000 1000")
    viewbox = models.CharField(
        max_length=50, 
        default="0 0 1000 1000", 
        help_text="Dimensiones originales del lienzo SVG para el escalado dinámico."
    )

    def __str__(self):
        return self.name


class Address(models.Model):
    # Relación uno a uno o Clave Foránea apuntando al lugar. 
    # Usamos OneToOneField si cada lugar tiene una única dirección física.
    place = models.OneToOneField(ShowPlace, on_delete=models.CASCADE, related_name="address")
    street = models.CharField(max_length=255, verbose_name="Calle y Número")
    city = models.CharField(max_length=100, verbose_name="Ciudad")
    state = models.CharField(max_length=100, verbose_name="Provincia/Estado")
    country = models.CharField(max_length=100, verbose_name="País", default="Argentina")
    zip_code = models.CharField(max_length=20, verbose_name="Código Postal", blank=True, null=True)

    def __str__(self):
        return f"{self.street}, {self.city}"

class Sector(models.Model):
    place = models.ForeignKey(ShowPlace, on_delete=models.CASCADE, related_name="sectors", verbose_name="Lugar")
    name = models.CharField(max_length=100, verbose_name="Nombre del Sector")
    slug = models.SlugField(max_length=100, help_text="Identificador único para el ID del SVG.")
    capacity = models.PositiveIntegerField(verbose_name="Capacidad Máxima Física del Sector")
    polygon_geometry = models.JSONField(
        verbose_name="Medidas del Polígono (JSON)",
        help_text="Diccionario con el tipo de forma de SVG y sus puntos/coordenadas correspondientes."
    )

    def __str__(self):
        return f"{self.place.name} - {self.name}"


class MapLayoutObject(models.Model):
    place = models.ForeignKey(ShowPlace, on_delete=models.CASCADE, related_name='layout_objects')
    name = models.CharField(max_length=100)
    # Guardamos una marca para saber si requiere etiqueta de texto (ej: 'STAGE')
    object_type = models.CharField(max_length=20, default='INFRA') 
    geometry = models.JSONField()

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre de la Categoría")
    # El slug sirve para armar URLs estéticas (ej: 'rock-internacional', 'teatro', 'electronica')
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Slug / Identificador URL")
    
    # ATRIBUTOS ESPECÍFICOS DE DISEÑO (Opcionales pero muy útiles)
    icon_class = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        help_text="Clase de FontAwesome o Bootstrap Icons (ej: 'bi-music-note-beamed')."
    )
    color_hex = models.CharField(
        max_length=7, 
        default="#007bff", 
        help_text="Color en formato HEX para las etiquetas del frontend (ej: '#ffc107')."
    )

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.name


class Show(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image_url = models.URLField(blank=True, null=True)

    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="shows",
        verbose_name="Categoría"
    )

    def __str__(self):
        return self.title



# NUEVO MODELO: Lógica comercial por cada función/Show
class ShowSector(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name="show_sectors")
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name="show_sectors")
    
    # El precio ahora depende del show dinámicamente
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Precio para este Show")
    
    # El inventario se controla por función, no por estadio fijo
    sold = models.PositiveIntegerField(default=0, verbose_name="Entradas Vendidas")
    reserved = models.PositiveIntegerField(default=0, verbose_name="Entradas Reservadas")
    available = models.PositiveIntegerField(default=0, verbose_name="Entradas Disponibles")

    class Meta:
        # Evita que para un mismo Show se duplique el mismo Sector
        unique_together = ('show', 'sector')

    def save(self, *args, **kwargs):
        # Lógica de negocio heredada: Validar contra la capacidad física del sector
        self.available = self.sector.capacity - (self.sold + self.reserved)
        
        if self.available < 0:
            raise ValidationError(f"La cantidad supera la capacidad física de {self.sector.name} ({self.sector.capacity}).")
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.show.title} - {self.sector.name} (${self.price})"