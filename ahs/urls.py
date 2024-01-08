from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('favicon.ico',  RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'))),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('core.urls'), name='core'),
    path('api/', include('api.urls'), name='api'),
    path('__debug__/', include('debug_toolbar.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
