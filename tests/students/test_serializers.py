import pytest

from django.contrib.auth import get_user_model
from django.test import TestCase

from students.models import Student
from students.serializers import StudentSerializer, StudentUpdateSerializer

USER = get_user_model()


class TestStudentSerializer(TestCase):
    """
    Test case for StudentSerializer
    """
    def setUp(self):
        self.email = 'test@gmail.com'
        self.first_name = 'test'
        self.last_name = 'Fisrt'
        self.user_type = 'S'

    def test_serializer_with_queryset(self):
        """
        Test case for serializer when queryset is present
        """
        self.user = USER.objects.create(
            first_name=self.first_name, last_name=self.last_name,
            email=self.email, user_type=self.user_type,
            is_active=1,
        )
        queryset = Student.objects.all()
        serializer = StudentSerializer(instance=queryset, many=True)
        self.assertEqual(1, len(serializer.data))
        for data in serializer.data:
            self.assertEqual(data['user']['first_name'], self.first_name)
            self.assertEqual(data['user']['last_name'], self.last_name)
            self.assertEqual(data['user']['user_type'], 'Student')
            self.assertEqual(data['user']['email'], self.email)

    def test_serializer_without_queryset(self):
        """
        Test case for serializer when queryset is present
        """
        queryset = Student.objects.all()
        serializer = StudentSerializer(instance=queryset, many=True)
        self.assertListEqual(serializer.data, [])


class TestStudentUpdateSerializer(TestCase):
    """
    Test case for StudentUpdateSerializer
    """
    def setUp(self):
        self.email = 'test@gmail.com'
        self.first_name = 'test'
        self.last_name = 'Fisrt'
        self.user_type = 'S'

    def test_serializer_with_queryset(self):
        """
        Test case for serializer when queryset is present
        """
        self.user = USER.objects.create(
            first_name=self.first_name, last_name=self.last_name,
            email=self.email, user_type=self.user_type,
            is_active=1,
        )
        validated_data = {"first_name": "Test 1", "last_name": "Test"}
        queryset = Student .objects.first()
        serializer = StudentUpdateSerializer(instance=queryset)
        serializer.data['user']['first_name'] = validated_data['first_name']
        serializer.data['user']['last_name'] = validated_data['last_name']
        instance = serializer.update(queryset, serializer.data)
        self.assertEqual(instance.id, queryset.id)
        self.assertEqual(instance.user.first_name, validated_data['first_name'])
        self.assertEqual(instance.user.last_name, validated_data['last_name'])
