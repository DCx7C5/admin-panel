from django.urls import path
from django.views.generic import TemplateView

from core.consumer import TerminalWorker
from core.views import DashboardView


urlpatterns = [
    path('', DashboardView.as_view(), name='core'),
    path('terminal/', TerminalWorker.as_asgi(), name='terminal'),
]
