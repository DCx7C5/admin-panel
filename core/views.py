import logging
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView


logger = logging.getLogger(__name__)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/index.html'


class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'settings/index.html'


class UserProfileView(LoginRequiredMixin, DetailView):
    http_method_names = ('GET', 'POST')
    model = get_user_model()
    template_name = "profile/index.html"

    async def get_context_data(self, **kwargs):
        ctx = await super().get_context_data(**kwargs)
        ctx['username'] = self.request.user.username
        return ctx

