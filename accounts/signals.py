from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save

from rest_framework.authtoken.models import Token

from students.models import Student
from teachers.models import Teacher

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 'S':
            Student.objects.create(user=instance)
        elif instance.user_type == 'T':
            Teacher.objects.create(user=instance)
