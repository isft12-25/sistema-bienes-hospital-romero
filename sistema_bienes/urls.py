from django.contrib import admin
<<<<<<< HEAD
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # ← INCLUIR las URLs de core
=======
from django.conf import settings
from django.urls import path, include
from .admin import custom_admin_site

urlpatterns = [
    path('admin/', custom_admin_site.urls),  # 👈 Admin agregado
    path('', include('core.urls')),   # Tu app principal
>>>>>>> d3a3fd8fbbadc8fa7b9dc0494193b2dbe96a2e20
]

# Debug Toolbar
if settings.DEBUG:
<<<<<<< HEAD
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
=======
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
>>>>>>> d3a3fd8fbbadc8fa7b9dc0494193b2dbe96a2e20
