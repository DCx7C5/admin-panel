import logging

from adrf.decorators import api_view
from adrf.viewsets import ViewSetMixin
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from rest_framework.decorators import authentication_classes, action
from adrf.views import APIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response as RESTResponse
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.serializers import HostSerializer, AHSUserSerializer

logger = logging.getLogger(__name__)

AHSUser = get_user_model()


@authentication_classes([SessionAuthentication])
@api_view(http_method_names=['get'])
async def get_user_data(request: HttpRequest):
    user_data = AHSUserSerializer(request.user).data
    return RESTResponse(user_data)


class ApiHostsView(APIView):
    permission_classes = [IsAuthenticated]
    view_is_async = True

    async def get(self, request) -> RESTResponse:
        logger.debug(f'{self.view_is_async}')
        serializer = HostSerializer(data=request.data)
        serializer.is_valid()
        return RESTResponse(await serializer.adata)
