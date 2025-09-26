from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from .admin import custom_admin_site

urlpatterns = [
    path('admin/', custom_admin_site.urls),  # 👈 Admin agregado
    path('', include('core.urls')),   # Tu app principal
]

# Debug Toolbar
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
