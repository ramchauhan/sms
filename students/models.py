from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Student(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )

    def __str__(self):
        return str(self.id)
