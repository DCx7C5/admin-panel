from django.urls import path
from django.views.generic import TemplateView

from core.consumer import TerminalConsumer
from core.views import DashboardView


urlpatterns = [
    path('', DashboardView.as_view(), name='core'),
    path('terminal/', TerminalConsumer.as_asgi(), name='terminal'),
    path('hello/', TemplateView.as_view(template_name='hello.html'))
]
