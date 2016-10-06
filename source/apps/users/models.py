# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.encoding import python_2_unicode_compatible


class UserManager(BaseUserManager):

    def create_user(self, email, display_name, password=None, **extra_fields):
        user = self.model(
            email = email,
            display_name = display_name,
            **extra_fields
        )
        user.set_password(password)
        user.full_clean()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, display_name, password, **extra_fields):
        return self.create_user(email, display_name, password, role=3, **extra_fields)


@python_2_unicode_compatible
class User(AbstractBaseUser):
    
    ROLES = (
        (0, 'Inactivo'),
        (1, 'Consultor'),
        (2, 'Operador'),
        (3, 'Administrador'),
    )
    
    email = models.EmailField(verbose_name='correo electrónico', unique=True)
    display_name = models.CharField(verbose_name='nombre', max_length=50, blank=True)
    
    date_created = models.DateTimeField(auto_now_add=True)
    role = models.PositiveIntegerField(verbose_name='rol', choices=ROLES, default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ()
    
    objects = UserManager()

    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'
    
    def __str__(self):
        return self.get_short_name()
    
    def get_full_name(self):
        return self.display_name
    get_full_name.short_description = 'nombre completo'

    def get_short_name(self):
        return self.email
    get_short_name.short_description = 'email'

    @property
    def traceable_name(self):
        return '{} [{}:{}]'.format(self.get_full_name(), self.get_role_display(), self.email)
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
    
    @property
    def is_active(self):
        return self.role >= 1
    
    @property
    def is_staff(self):
        return self.role >= 2
    
    @property
    def is_superuser(self):
        return self.role >= 3

    @property
    def is_consultor(self):
        return self.role == 1

    def get_absolute_url(self):
        if self.is_consultor:
            return 'frontend_dashboard'
        elif self.is_staff or self.is_superuser:
            return 'backend_dashboard'
        return settings.LOGIN_URL
