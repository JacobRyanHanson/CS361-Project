from datetime import date, datetime
import os
from unittest.mock import MagicMock

import django
from django.test import TestCase, Client

from TA_Scheduling_App.models import User, Course

# Set up the Django settings module for testing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TA_Scheduling_Project.settings')
django.setup()


class TestUserCreation(TestCase):
    monkey = None

    def setUp(self):
        self.monkey = Client()

        self.admin = User(
            ROLE='ADMIN',
            FIRST_NAME='John',
            LAST_NAME='Doe',
            EMAIL='admin@example.com',
            PASSWORD_HASH='ad_password',
            PHONE_NUMBER='555-123-4567',
            ADDRESS='123 Main St',
            BIRTH_DATE=date(1990, 1, 1)
        )

        self.admin.save()

        self.credentials = {
            "email": "admin@example.com",
            "password": "ad_password"
        }

        self.monkey.post("/", self.credentials, follow=True)

    def test_AddNewTA(self):
        response = self.monkey.post('/user-creation/', {'role': "TA",
                                                        'firstName': "Joe",
                                                        'lastName': "Smoe",
                                                        'email': "joeSmoe@gmail.com",
                                                        'phoneNumber': "999-999-9999",
                                                        'address': "101 Drive",
                                                        'birthDate': date(1990, 1, 1)})
        self.assertEqual(response.context['status'], 'Successfully created the user.')

    def test_AddNewInstr(self):
        response = self.monkey.post('/user-creation/', {'role': "INSTRUCTOR",
                                                        'firstName': "Jeff",
                                                        'lastName': "Smoe",
                                                        'email': "jeffSmoe@gmail.com",
                                                        'phoneNumber': "999-999-9998",
                                                        'address': "102 Drive",
                                                        'birthDate': date(1990, 1, 2)})
        self.assertEqual(response.context['status'], 'Successfully created the user.')

    def test_InvalidEmail(self):
        response = self.monkey.post('/user-creation/', {'role': "TA",
                                                        'firstName': "Joe",
                                                        'lastName': "Smoe",
                                                        'email': "admin@example.com",
                                                        'phoneNumber': "999-999-9999",
                                                        'address': "101 Drive",
                                                        'birthDate': date(1990, 1, 1)})
        self.assertEqual(response.context['status'], 'Users with duplicate emails are not allowed.')

    def test_InvalidRole(self):
        response = self.monkey.post('/user-creation/', {'role': "",
                                                        'firstName': "Joe",
                                                        'lastName': "Smoe",
                                                        'email': "admin@example.com",
                                                        'phoneNumber': "999-999-9999",
                                                        'address': "101 Drive",
                                                        'birthDate': date(1990, 1, 1)})
        self.assertEqual(str(response.context['status']), 'Invalid role')
