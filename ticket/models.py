from django.db import models
from shows.models import Show

class Ticket(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='tickets')
    buyer_name = models.CharField(max_length=150)
    buyer_email = models.EmailField()
    purchase_date = models.DateTimeField(auto_now_add=True)
    seat_number = models.CharField(max_length=20)
    checked_in = models.BooleanField(default=False)

    def __str__(self):
        return f"Ticket for {self.show.title} - {self.buyer_name} ({self.seat_number})"
