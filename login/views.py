from django.shortcuts import (
    render,
    redirect
)
from django.db import connection
from .models import LoginLog

import random
from django.contrib import messages
from register.utils import (
    send_activation_email
)

from django.contrib.auth import (
    authenticate,
    login,
    logout
)
from django.views.decorators.http import (
    require_POST
)

from django.core.mail import (
    EmailMessage
)

from .models import LoginCode
from register.models import User
from register.decorators import (
    unauthenticated_user
)

import json
import random
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage

@unauthenticated_user
def login_view(request):
    if request.method == 'POST':
        # Detectamos si viene por Fetch (JavaScript)
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
        
        if is_ajax:
            # Si viene por JS, los datos viajan en el cuerpo (body) en formato JSON
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
        else:
            # Por si acaso entra un POST tradicional
            email = request.POST.get('email')
            password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user and user.check_password(password):
            if not user.is_active:
                request.session['inactive_user_id'] = user.id
                
                if is_ajax:
                    return JsonResponse({'success': True, 'redirect_url': 'account-not-verified/'}) # O el nombre de tu ruta
                return redirect('account-not-verified')

            # GENERAR CODIGO
            code = str(random.randint(100000, 999999))

            # BORRAR CODIGOS VIEJOS
            LoginCode.objects.filter(user=user).delete()

            # GUARDAR NUEVO CODIGO
            LoginCode.objects.create(user=user, code=code)

            # ENVIAR EMAIL
            email_message = EmailMessage(
                'Código de acceso',
                f'Tu código es: {code}',
                to=[user.email]
            )
            email_message.send()

            # SESSION TEMPORAL
            request.session['login_user_id'] = user.id

            if is_ajax:
                # Éxito: Le decimos a JS a dónde mandar al usuario a poner el código
                return JsonResponse({'success': True, 'redirect_url': 'verify-login/'}) # Asegura que apunte a tu URL real
            return redirect('verify-login')
            
        else:
            # CREDENCIALES INVÁLIDAS
            if is_ajax:
                return JsonResponse({'success': False, 'message': 'Credenciales inválidas. Por favor, intentá de nuevo.'})
            return render(request, 'login/login.html', {'error': 'Credenciales inválidas'})

    return render(request, 'login/login.html')

def account_not_verified_view(request):
    user_id = request.session.get(
        'inactive_user_id'
    )

    if not user_id:
        return redirect('login')

    user = User.objects.get(
        id=user_id
    )
    return render(
        request,
        'login/account_not_verified.html',
        {
            'user': user
        }
    )


def resend_activation_email_view(request):
    user_id = request.session.get(
        'inactive_user_id'
    )

    if not user_id:
        return redirect('login')

    user = User.objects.get(
        id=user_id
    )

    send_activation_email(
        request,
        user
    )

    messages.success(
        request,
        'Te reenviamos el email de activación.'
    )
    return redirect(
        'account-not-verified'
    )

@unauthenticated_user
def verify_login_code_view(request):
    user_id = request.session.get(
        'login_user_id'
    )

    if not user_id:
        return redirect('login')

    user = User.objects.get(
        id=user_id
    )

    if request.method == 'POST':
        code = request.POST.get(
            'code'
        )
        login_code = LoginCode.objects.filter(
            user=user,
            code=code
        ).first()

        if login_code:
            login_code.delete()
            request.session.pop(
                'login_user_id',
                None
            )
            login(request, user)
            return redirect('/')

        else:
            return render(
                request,
                'login/verify_login.html',
                {
                    'error':
                    'Código inválido'
                }
            )

    return render(
        request,
        'login/verify_login.html'
    )

@require_POST
def logout_view(request):
    logout(request)
    return redirect('/')
