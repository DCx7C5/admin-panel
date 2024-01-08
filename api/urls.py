from django.urls import path
from api.views import ApiHostsView, get_user_data


app_name = 'api'


urlpatterns = [
    path('hosts/', ApiHostsView.as_view(), name='hosts_list'),
    path('user/', get_user_data, name='user_data'),
]
