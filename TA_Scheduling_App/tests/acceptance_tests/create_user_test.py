import datetime
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

    def test_AddNewUser(self):
        session = self.monkey.session
        session['session_email'] = 'john.doe@example.com'
        session.save()
        response = self.monkey.post('/user-creation/', {'ROLE': "TA",
                                                        'FIRST_NAME': "Joe",
                                                        'LAST_NAME': "Smoe",
                                                        'EMAIL': "joeSmoe@gmail.com",
                                                        'PHONE_NUMBER': "999-999-9999",
                                                        'ADDRESS': "101 Drive",
                                                        'BIRTH_DATE': datetime.date.today()})
        self.assertTrue(response, "New User was not added correctly")

    def test_InvalidInput(self):
        session = self.monkey.session
        session['session_email'] = 'john.doe@example.com'
        session.save()
        response = self.monkey.post('/user-creation/', {'ROLE': "TA",
                                                        'FIRST_NAME': "",
                                                        'LAST_NAME': "Smoe",
                                                        'EMAIL': "joeSmoe@gmail.com",
                                                        'PHONE_NUMBER': "999-999-9999",
                                                        'ADDRESS': "101 Drive",
                                                        'BIRTH_DATE': datetime.date.today()})
        self.assertContains(response, 'This field is required.')
