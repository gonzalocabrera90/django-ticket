from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from main.views import error_404_redirect_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    #path('', include('home.urls')),
    path('login/', include('login.urls')),
    path('register/', include('register.urls')),
    path('shows/', include('shows.urls')),
    path('ticket/', include('ticket.urls')),
]

# si la url no se encuentra en el proyecto se redirecciona a "/"
# funciona con DEBUG = False
handler404 = error_404_redirect_view

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
