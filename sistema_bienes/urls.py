from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from .admin import custom_admin_site

urlpatterns = [
    path('admin/', custom_admin_site.urls),  # Admin personalizado
    path('', include('core.urls')),          # App principal
]

# Debug Toolbar y archivos estáticos
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
