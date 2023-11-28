import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    """
    Simple subclass for custom field extensions of :class: User
    """

    date_modified = models.DateTimeField(
        help_text='Last time the user profile was updated',
        verbose_name='date modified',
        auto_now=True,
        blank=False,
        null=False,
    )

    uid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False,
        blank=False,
        null=False,
        db_index=True,
    )

    image = models.ImageField(
        verbose_name='profile picture'
    )

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
