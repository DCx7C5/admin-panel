from __future__ import annotations

from django.db.models import (
    CharField,
    ForeignKey,
    CASCADE,
    BooleanField,
    DateTimeField,
    GenericIPAddressField,
    Model,
    QuerySet,
    Manager,
)

from ahs import settings


User = settings.AUTH_USER_MODEL


class EndPointManager(Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset()


class Endpoint(Model):
    segment = CharField(
        max_length=32,
        verbose_name='path segment',
    )
    name = CharField(
        max_length=255,
        unique=True,
    )
    parent = ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=CASCADE,
        related_name='children',
    )

    def __str__(self):
        return self.name

    def is_root(self):
        return not self.parent

    def has_children(self):
        return self.children.exists()

    def get_ancestors(self):
        ancestors = [self]
        current_parent = self.parent

        while current_parent:
            ancestors.insert(0, current_parent)
            current_parent = current_parent.parent

        return ancestors

    def get_descendants(self):
        descendants = []

        for child in self.children.all():
            descendants.append(child)
            descendants.extend(child.get_descendants())

        return descendants

    objects = Manager

    class Meta:
        app_label = 'core'
        verbose_name = 'url endpoint'
        verbose_name_plural = 'url_endpoints'


class HostManager(Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset()


class RemoteHostManager(Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(remote=True)

    def create_rhost(self, address, name, owner, remote=True, *args, **kwargs):
        return self.acreate(address=address, name=name, owner=owner, remote=remote, *args, **kwargs)

    def get_or_create_rhost(self, defaults=None, **kwargs) -> Host:
        return self.aget_or_create(defaults, **kwargs)


class Host(Model):

    address = GenericIPAddressField(
        verbose_name='host ip address',
        unique=True,
        blank=False,
        protocol='IPv4',
    )
    name = CharField(
        verbose_name='hostname',
        max_length=253,
        unique=True,
        blank=True,
    )
    owner = ForeignKey(
        to=User,
        on_delete=CASCADE,
    )
    remote = BooleanField(
        verbose_name='is remote host',
    )

    created = DateTimeField(
        verbose_name='created on',
        auto_now_add=True,
    )

    updated = DateTimeField(
        verbose_name='last update on',
        auto_now=True,
    )

    objects = Manager()
    remote_hosts = RemoteHostManager()

    class Meta:
        app_label = 'core'
        verbose_name = 'host'
        verbose_name_plural = 'hosts'

    async def adelete(self, using=None, keep_parents=False):
        await super().adelete(using, keep_parents)

    async def asave(self, *args, **kwargs):
        await super().asave(*args, **kwargs)
