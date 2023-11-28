from django.urls import path
from django.views.generic import TemplateView

from core.views import DashboardView


urlpatterns = [
    path('', DashboardView.as_view(), name='core'),
    path('hello/', TemplateView.as_view(template_name='hello.html'))
]
