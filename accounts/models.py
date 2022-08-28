from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    personal_id = models.CharField(max_length=8, unique=True)
    full_name = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=11, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'personal_id'
    REQUIRED_FIELDS = ['email', 'full_name', 'phone_number', ]

    objects = UserManager()

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return f'{self.personal_id} - {self.full_name}'
