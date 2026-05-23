from django.contrib import admin

# Register your models here.

# from .models import (
#     Country,
#     Province,
#     City,
#     Address,
#     User
# )
# from cities_light.models import (

#     Country,
#     Region,
#     City

# )
from .models import (
    Address,
    User
)

# admin.site.register(Country)

# admin.site.register(Region)

# admin.site.register(City)

admin.site.register(Address)

admin.site.register(User)