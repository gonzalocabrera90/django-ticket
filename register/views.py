from django.db import connection
from django.http import JsonResponse

from cities_light.models import Country
from cities_light.models import Region
from cities_light.models import City

from django.shortcuts import (
    render,
    redirect
)

from django.contrib.auth import login

from .forms import (
    RegisterForm,
    AddressForm
)

def register_view(request):

    if request.method == 'POST':

        form = RegisterForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            user = form.save()

            # LOGIN AUTOMATICO

            login(request, user)

            return redirect(
                'address-register'
            )

    else:

        form = RegisterForm()

    return render(
        request,
        'register/register.html',
        {
            'form': form
        }
    )

def address_register_view(request):

    if not request.user.is_authenticated:

        return redirect('register')

    if request.method == 'POST':

        form = AddressForm(request.POST)

        if form.is_valid():

            address = form.save()

            user = request.user

            user.address = address

            user.save()

            return redirect('/')

    else:

        form = AddressForm()

    countries = Country.objects.all()

    return render(
        request,
        'register/address.html',
        {
            'form': form,
            'countries': countries
        }
    )

def load_regions(request):

    country_id = request.GET.get('country')

    regions = Region.objects.filter(
        country_id=country_id
    ).values(
        'id',
        'name'
    )

    return JsonResponse(
        list(regions),
        safe=False
    )

def load_cities(request):

    region_id = request.GET.get('region')

    cities = City.objects.filter(
        region_id=region_id
    ).values(
        'id',
        'name'
    ).order_by('name')

    return JsonResponse(
        list(cities),
        safe=False
    )