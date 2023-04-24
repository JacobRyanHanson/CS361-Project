import datetime
import os
from unittest.mock import MagicMock

import django
from django.test import TestCase, Client

from TA_Scheduling_App.models import User, Course

# Set up the Django settings module for testing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TA_Scheduling_Project.settings')
django.setup()


class TestCreateSection(TestCase):
    monkey = None

    def setUp(self):
        self.monkey = Client()

    def test_BadCourse(self):
        session = self.monkey.session
        session['session_email'] = 'john.doe@example.com'
        session.save()
        response = self.monkey.post("/section-creation/", {"SECTION_NUMBER": 901,
                                                           "COURSE": '',
                                                           "BUILDING": 'Chemistry Building',
                                                           "ROOM_NUMBER": '190',
                                                           "SECTION_START": datetime.time(9, 30),
                                                           "SECTION_END": datetime.time(10, 20)}, follow=True)
        self.assertRaises(ValueError, response, "Section should not have been created")

    def test_MissingInfo(self):
        session = self.monkey.session
        session['session_email'] = 'john.doe@example.com'
        session.save()
        response = self.monkey.post("/section-creation/", {"SECTION_NUMBER": 901,
                                                           "COURSE": "120",
                                                           "BUILDING": '',
                                                           "ROOM_NUMBER": '190',
                                                           "SECTION_START": datetime.time(9, 30),
                                                           "SECTION_END": datetime.time(10, 20)}, follow=True)
        self.assertContains(response, 'This field is required.')

    def test_SectionCreated(self):
        session = self.monkey.session
        session['session_email'] = 'john.doe@example.com'
        session.save()
        response = self.monkey.post("/section-creation/", {"SECTION_NUMBER": 901,
                                                           "COURSE": "120",
                                                           "BUILDING": 'Chemistry Building',
                                                           "ROOM_NUMBER": '190',
                                                           "SECTION_START": datetime.time(9, 30),
                                                           "SECTION_END": datetime.time(10, 20)}, follow=True)
        self.assertTrue(response, "section not added")
