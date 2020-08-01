import json
import pytest
import requests

from unittest import mock

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from students.models import Student
from students.views import StudentViewSet

USER = get_user_model()


class StudentViewSetTest(APITestCase):
    """
    Test case for StudentView Set
    """
    def setUp(self):
        # User Setup
        self.first_name = 'test 1'
        self.last_name = "testing"
        self.email = 'test@sms.com'
        self.password = '12426637dsfsA@#'

        self.user = USER(
            first_name=self.first_name, last_name=self.last_name,
            email=self.email, user_type="S", is_active=1,
        )
        self.user.set_password(self.password)
        self.user.save()

    def get_login_response(self):
        headers = {'Content-Type': 'application/json'}
        try:
            url = reverse('auth-login')
            response = self.client.post(
                url,
                data={'email': self.email, 'password': self.password},
                headers=headers
            )
        except Exception as ex:
            print(ex)

        return response

    def test_list_students_with_valid_token(self):
        headers = {'Content-Type': 'application/json'}
        response = self.get_login_response()

        self.client.credentials(
            HTTP_AUTHORIZATION=f"""Token {response.data['token']}"""
        )
        response = self.client.get(reverse('students-list'))
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data[0]['id'], 1)
        self.assertEqual(response_data[0]['user']['id'], self.user.id)
        self.assertEqual(response_data[0]['user']['email'], self.user.email)
        self.assertEqual(response_data[0]['user']['user_type'], 'Student')
        self.assertEqual(
            response_data[0]['user']['first_name'], self.user.first_name
        )

    def test_list_students_with_invalid_token(self):
        headers = {'Content-Type': 'application/json'}

        self.client.credentials(
            HTTP_AUTHORIZATION=f"""Token sjjksjkds903093903"""
        )
        response = self.client.get(reverse('students-list'))
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response_data['detail'], 'Invalid token.')

    def test_students_detail_with_valid_token(self):
        headers = {'Content-Type': 'application/json'}
        response = self.get_login_response()

        self.client.credentials(
            HTTP_AUTHORIZATION=f"""Token {response.data['token']}"""
        )
        response = self.client.get(reverse(
            'students-detail', kwargs={'pk': Student.objects.first().id}
        ))
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['id'], 1)
        self.assertEqual(response_data['user']['id'], self.user.id)
        self.assertEqual(response_data['user']['email'], self.user.email)
        self.assertEqual(response_data['user']['user_type'], 'Student')
        self.assertEqual(
            response_data['user']['first_name'], self.user.first_name
        )

    def test_students_update_with_valid_token(self):
        headers = {'Content-Type': 'application/json'}
        response = self.get_login_response()

        self.client.credentials(
            HTTP_AUTHORIZATION=f"""Token {response.data['token']}"""
        )
        data = {
            "user": {
                "username": "Test 1",
                "first_name": "Test Update",
                "last_name": "Test",
                "is_active": True
            }
        }
        response = self.client.put(
            path=reverse(
                'students-detail', kwargs={'pk': Student.objects.first().id}
            ),
            data=data, format='json',
            headers=headers
        )
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['id'], 1)
        self.assertEqual(response_data['user']['id'], self.user.id)
        self.assertEqual(response_data['user']['email'], self.user.email)
        self.assertEqual(
            response_data['user']['first_name'], data['user']['first_name']
        )
        self.assertEqual(
            response_data['user']['username'], data['user']['username']
        )

    def test_list_students_with_different_user_type(self):
        headers = {'Content-Type': 'application/json'}
        response = self.get_login_response()

        self.client.credentials(
            HTTP_AUTHORIZATION=f"""Token {response.data['token']}"""
        )
        self.user.user_type = 'T'
        self.user.save()
        response = self.client.get(reverse('students-list'))
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data[0]['id'], 1)
        self.assertEqual(response_data[0]['user']['id'], self.user.id)
        self.assertEqual(response_data[0]['user']['email'], self.user.email)
        self.assertEqual(response_data[0]['user']['user_type'], 'Teacher')
        self.assertEqual(
            response_data[0]['user']['first_name'], self.user.first_name
        )
