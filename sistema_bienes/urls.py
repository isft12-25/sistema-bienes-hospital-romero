from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from .admin import custom_admin_site  # o usa admin si no existe el custom
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', custom_admin_site.urls),  # o admin.site.urls
    path('', include('core.urls')),
]

if settings.DEBUG:
    try:
        import debug_toolbar
        urlpatterns += [ path('__debug__/', include(debug_toolbar.urls)) ]
    except ImportError:
        pass
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
