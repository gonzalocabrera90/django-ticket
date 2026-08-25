import os

from django.template.loader import (
    render_to_string
)

from django.urls import reverse

from django.utils.http import (
    urlsafe_base64_encode
)

from django.utils.encoding import (
    force_bytes
)

from django.contrib.auth.tokens import (
    default_token_generator
)

def send_activation_email(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    
    # 1. Obtenemos la ruta relativa (/register/activate/MQ/token/)
    relative_path = reverse(
        'activate-account',
        kwargs={
            'uidb64': uid,
            'token': token
        }
    )

    # 2. Construcción dinámica del dominio según el entorno
    # GitHub Codespaces envía la URL pública en el header X-Forwarded-Host
    forwarded_host = request.META.get('HTTP_X_FORWARDED_HOST')
    codespace_name = os.environ.get('CODESPACE_NAME')

    if forwarded_host:
        # Petición a través del proxy de Codespaces o servidor de producción
        activation_link = f"https://{forwarded_host}{relative_path}"
    elif codespace_name:
        # Fallback si estamos en Codespaces pero el header no se transmitió
        activation_link = f"https://{codespace_name}-8000.app.github.dev{relative_path}"
    else:
        # Entorno Local estándar (Windows / Linux sin proxy)
        activation_link = request.build_absolute_uri(relative_path)

    html_content = render_to_string(
        'register/activation_email.html',
        {
            'user': user,
            'activation_link': activation_link
        }

    )

    print('\n')
    print('================ EMAIL =================')
    print(html_content)
    print('========================================')
    print('\n')