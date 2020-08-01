from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

from rest_framework.test import APITestCase

from students.models import Student

USER = get_user_model()


class TestStudentModel(APITestCase):
    def setUp(self):
        self.email = 'test@gmail.com'
        self.first_name = 'test'
        self.last_name = 'Fisrt'
        self.user_type = 'S'
        self.user = USER.objects.create(
            first_name=self.first_name, last_name=self.last_name,
            email=self.email, user_type=self.user_type,
            is_active=1,
        )
    def test_student_created(self):
        user = USER.objects.get(email=self.email)
        self.assertEqual(user.first_name, self.first_name)
        self.assertEqual(user.last_name, self.last_name)
        self.assertEqual(user.is_active, 1)
        self.assertEqual(Student.objects.all().count(), 1)

    def test_unique_user_email(self):
        with self.assertRaises(IntegrityError):
            user = USER.objects.create(
                first_name=self.first_name, email=self.email,
                user_type='T', is_active=1,
            )
