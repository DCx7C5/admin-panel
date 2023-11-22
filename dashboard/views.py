from asgiref.typing import HTTPRequestEvent
from django.views.generic import ListView, TemplateView


class DashboardView(TemplateView):
    template_name = 'dashboard/index.html'
