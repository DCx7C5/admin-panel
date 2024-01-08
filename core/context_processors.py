import logging

from django.contrib.auth.models import AnonymousUser
from django.db.models import Manager
from django.http import HttpRequest

from api.serializers import AHSUserSerializer
from core.models import Endpoint


logger = logging.getLogger(__name__)


def endpoints(request: HttpRequest):
    request.user if request.user else AnonymousUser()

    manager: Manager = getattr(Endpoint, 'objects')
    _endpoints = manager.all()
    return {'ENDPOINTS': _endpoints}


def all_urls(request: HttpRequest):
    func = request.build_absolute_uri
    return {
        'ABSOLUTE_ROOT': func('/')[:-1].strip('/'),
        'ABSOLUTE_ROOT_URL': func('/').strip('/'),
        'FULL_URL_INCL_PATH': func(),
        'FULL_URL': func('?')
    }


def all(request: HttpRequest):
    kwargs = {}
    urls = all_urls(request)
    for url in urls.keys():
        kwargs[url] = urls.pop(url)

    eps = endpoints(request)
    kwargs['ENDPOINTS'] = eps.pop('ENDPOINTS')
    return kwargs


def ahs_serialized_userdata(request: HttpRequest):
    user_data = AHSUserSerializer(request.user).data
    return {'AHS_SERIAL_USER': user_data}
