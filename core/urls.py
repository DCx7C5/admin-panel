from django.urls import path, re_path
from core.views import DashboardView, hosts_list, ApiHostsView

urlpatterns = [
    path('', DashboardView.as_view(), name='core'),
    re_path(r'^api/hosts/$', ApiHostsView.as_view(), name='hosts_list'),
]
