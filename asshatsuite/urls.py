from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include("django.contrib.auth.urls")),
    path('', include('core.urls')),
    path('__debug__/', include("debug_toolbar.urls")),
]
