from django.conf import settings
from django.urls import include, path
from .admin import custom_admin_site

urlpatterns = [
    path("admin/", custom_admin_site.urls),
	path("", include("core.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
