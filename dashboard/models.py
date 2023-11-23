from __future__ import annotations

from django.contrib.auth import get_user_model
from django.db.models import (
    Model,
    CharField,
    ForeignKey,
    CASCADE,
    BooleanField,
    GenericIPAddressField,
    DateTimeField, QuerySet, Manager, URLField,
)


CustomUser = get_user_model()


class SidebarItemManager(Manager):
    async def get_queryset(self):
        return await super().get_queryset().filter(context='SB')


class MenuItem(Model):

    name = CharField(
        max_length=50,
        unique=True,
        editable=True,
        null=False,
    )
    path = URLField(
        verbose_name='url path',
        default='/',
        editable=True,
    )
    context = CharField(
        max_length=2,
        choices=[('SB', 'Sidebar'), ],
        null=False,
        editable=True,
    )
    objects = Manager()
    sidebar_items = SidebarItemManager()

    class Meta:
        verbose_name = 'menu item'
        verbose_name_plural = 'menu items'
        managed: True


class HostManager(Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset()


class RemoteHostManager(Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(remote=True)

    async def create_rhost(self, address, name, owner, remote=True, *args, **kwargs):
        return await self.acreate(address=address, name=name, owner=owner, remote=remote, *args, **kwargs)

    async def get_or_create_rhost(self, defaults=None, **kwargs) -> Host:
        return await self.aget_or_create(defaults, **kwargs)


class Host(Model):

    address = GenericIPAddressField(
        verbose_name='host ip address',
        unique=True,
        editable=True,
    )
    name = CharField(
        verbose_name='hostname',
        max_length=253,
        unique=True,
        editable=True,
    )
    owner = ForeignKey(
        to=CustomUser,
        on_delete=CASCADE,
    )
    remote = BooleanField(
        verbose_name='is remote host',
        editable=False,
    )

    remote_hosts = RemoteHostManager()

    created = DateTimeField(
        verbose_name='created on',
        auto_now_add=True,
    )

    updated = DateTimeField(
        verbose_name='last update on',
        auto_now=True,
    )

    class Meta:
        managed = True
        verbose_name = 'host'
        verbose_name_plural = 'hosts'

    async def delete(self, using=None, keep_parents=False):
        await super().adelete(using, keep_parents)

    async def save(self, *args, **kwargs):
        await super().asave(*args, **kwargs)
