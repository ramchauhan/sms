from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, user_type, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not user_type:
            raise ValueError('Users must have an Type')

        user = self.model(
	        email=self.normalize_email(email),
            first_name=first_name,
            user_type=user_type,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, user_type, password):
    	user = self.create_user(
    	    email=email,
    	    password=password,
    	    first_name=first_name,
    	    user_type=user_type,
    	)
    	user.is_admin = True
    	user.is_staff = True
    	user.is_superuser = True
    	user.save(using=self._db)
    	return user


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('S', 'Student'),
	    ('T', 'Teacher'),
	    ('A', 'Admin'),
    )
    user_type = models.CharField(choices=USER_TYPE_CHOICES, max_length=3)
    username = models.CharField(max_length=100, blank=True)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'user_type']

    objects = UserManager()

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.email
