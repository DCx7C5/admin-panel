from __future__ import annotations
import uuid

from django.contrib.auth import get_user_model
from django.db.models import (
    Model,
    CharField,
    ForeignKey,
    CASCADE,
    BooleanField,
    GenericIPAddressField,
    UUIDField,
    Index,
    DateTimeField, QuerySet, Manager,
)


CustomUser = get_user_model()


class MenuItem(Model):
    id = UUIDField(
        primary_key=True,
        db_index=True,
        default=uuid.uuid4,
        editable=False
    )
    name = CharField(max_length=50)
    context = CharField(max_length=30)

    class Meta:
        indexes = [Index(fields=['id'], name='id_menuitem')]
        managed: True


class HostQuerySet(QuerySet):
    def remotes(self):
        return self.filter(remotes=True)

    def local(self):
        return self.filter(remotes=False)


class HostManager(Manager):

    async def get_queryset(self):
        return HostQuerySet(self.model, using=self._db)


class RemoteHostManager(Manager):
    async def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(remote=True)

    async def create_rhost(self, address, name, owner, remote=True, *args, **kwargs):
        return await self.acreate(address=address, name=name, owner=owner, remote=remote, *args, **kwargs)

    async def get_or_create_rhost(self, defaults=None, **kwargs) -> Host:
        return await self.aget_or_create(defaults, **kwargs)


class Host(Model):
    id = UUIDField(
        primary_key=True,
        db_index=True,
        default=uuid.uuid4,
        editable=False
    )
    address = GenericIPAddressField()
    name = CharField(
        max_length=253,
    )
    owner = ForeignKey(
        to=CustomUser,
        on_delete=CASCADE,
    )
    remote = BooleanField(
        verbose_name='is remote host',
    )
    hosts = HostManager()
    remote_hosts = RemoteHostManager()
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    class Meta:
        indexes = [Index(fields=['id'], name='id_host')]
        managed = True

    async def save(self, *args, **kwargs):
        await super().save(*args, **kwargs)
