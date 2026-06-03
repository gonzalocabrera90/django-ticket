from django.db import models
from shows.models import Show, ShowSector
import uuid
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pendiente de Pago'),
        ('PAID', 'Pagada / Confirmada'),
        ('EXPIRED', 'Expirada / Cancelada'),
        ('REFUNDED', 'Reembolsada'),
    ]

    # 2. Reemplazamos 'User' por settings.AUTH_USER_MODEL
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='orders'
    )
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='orders')
    show_sector = models.ForeignKey(ShowSector, on_delete=models.CASCADE, related_name='orders')
    
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Orden #{self.id} - {self.user.username} - {self.status}"


class Ticket(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='tickets')
    show_sector = models.ForeignKey(ShowSector, on_delete=models.CASCADE, related_name='tickets')
    
    ticket_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    
    # Corrección de max_digits a max_length
    attendee_name = models.CharField(max_length=100, blank=True, null=True)
    
    is_used = models.BooleanField(default=False)
    used_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Ticket {self.ticket_code} - Sector: {self.show_sector.sector.name}"
