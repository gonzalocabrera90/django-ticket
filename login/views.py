from django.shortcuts import (
    render,
    redirect
)
from django.db import connection
from .models import LoginLog

import random

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

# def login_view(request):
#     recent_logins = LoginLog.objects.order_by('-timestamp')[:5]
    
#     db_name = connection.settings_dict.get('NAME', 'N/A')
#     db_user = connection.settings_dict.get('USER', 'N/A')

#     context = {
#         'recent_logins': recent_logins,
#         'url_name': 'Login (/login)',
#         'current_url': '/login',
#         'db_name': db_name,
#         'db_user': db_user
#     }
#     return render(request, 'login/login.html', context)

@unauthenticated_user
def login_view(request):

    if request.method == 'POST':
        email = request.POST.get(
            'email'
        )
        password = request.POST.get(
            'password'
        )
        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is not None:
            if not user.is_active:
                # return render(
                #     request,
                #     'register/login.html',
                #     {
                #         'error':
                #         'Cuenta no activada'
                #     }
                # )
                request.session[
                    'inactive_user_id'
                ] = user.id

                return redirect(
                    'account-not-verified'
                )
            # GENERAR CODIGO

            code = str(
                random.randint(
                    100000,
                    999999
                )
            )

            # BORRAR CODIGOS VIEJOS
            LoginCode.objects.filter(
                user=user
            ).delete()

            # GUARDAR NUEVO CODIGO
            LoginCode.objects.create(
                user=user,
                code=code
            )

            # ENVIAR EMAIL
            email_message = EmailMessage(
                'Código de acceso',
                f'Tu código es: {code}',
                to=[user.email]
            )
            email_message.send()

            # SESSION TEMPORAL
            request.session[
                'login_user_id'
            ] = user.id

            return redirect(
                'verify-login'
            )

        else:
            return render(
                request,
                'login/login.html',
                {
                    'error':
                    'Credenciales inválidas'
                }
            )

    return render(
        request,
        'login/login.html'
    )

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
                'register/verify_login.html',
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