from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from students.models import Student

User = get_user_model()


class Teacher(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='teacher_profile'
    )
    students = models.ManyToManyField(
        Student,
        related_name='students'
    )
    birth_date = models.DateField(null=True, blank=True)
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    updated = models.DateTimeField(_("Updated"), auto_now=True)

    def __str__(self):
        return str(self.id)


class Rating(models.Model):
    """
    Model to represent the Student Rating
    """
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name='raitings'
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='raitins'
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    updated = models.DateTimeField(_("Updated"), auto_now=True)

    class Meta:
        unique_together = ('teacher', 'student')
