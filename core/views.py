from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from adrf.decorators import api_view
from adrf.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response

from core.models import Host
from core.serializers import HostSerializer


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'


@api_view(['GET', 'POST'])
async def hosts_list(request) -> Response:
    serializer = HostSerializer(data=request.data)
    if serializer.is_valid():
        return await serializer.adata


class ApiHostsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    async def get(self, request) -> Response:
        serializer = HostSerializer(data=request.data)
        serializer.is_valid()
        return Response(await serializer.adata)
