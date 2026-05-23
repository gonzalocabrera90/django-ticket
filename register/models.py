from django.db import models
from cities_light.models import City
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    username = None

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)

    birth = models.DateField()

    email = models.EmailField(unique=True)

    dni = models.CharField(
        max_length=20,
        unique=True
    )

    img = models.ImageField(
        upload_to='users/',
        blank=True,
        null=True
    )

    address = models.ForeignKey(
        'Address',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Address(models.Model):

    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE
    )

    street = models.CharField(max_length=200)

    street_number = models.CharField(max_length=20)

    floor = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    apartment = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    postal_code = models.CharField(max_length=20)

    def __str__(self):

        return (
            f"{self.street} "
            f"{self.street_number}"
        )

