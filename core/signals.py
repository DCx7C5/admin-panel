from django.dispatch import Signal

socket_conn_request = Signal()
socket_conn_accepted = Signal()
socket_conn_closed = Signal()
socket_conn_lost = Signal()
socket_conn_error = Signal()
from django.db.models.signals import Signal

my_signal = Signal()