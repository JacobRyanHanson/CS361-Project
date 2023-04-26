import datetime
import os

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

        self.admin = User(
            ROLE='ADMIN',
            FIRST_NAME='John',
            LAST_NAME='Doe',
            EMAIL='admin@example.com',
            PASSWORD_HASH='ad_password',
            PHONE_NUMBER='555-123-4567',
            ADDRESS='123 Main St',
            BIRTH_DATE=datetime.date(1990, 1, 1)
        )

        self.admin.save()

        user2 = User.objects.create(
            ROLE='INSTRUCTOR',
            FIRST_NAME='Alice',
            LAST_NAME='Smith',
            EMAIL='alice.smith@example.com',
            PASSWORD_HASH='<hashed_password>',
            PHONE_NUMBER='555-987-6543',
            ADDRESS='456 Elm St',
            BIRTH_DATE=datetime.date(1985, 6, 15)
        )

        user2.save()

        self.course = Course.objects.create(
            COURSE_NUMBER=101,
            INSTRUCTOR=user2,
            COURSE_NAME='Introduction to Computer Science',
            COURSE_DESCRIPTION='An introductory course to the world of computer science.',
            SEMESTER='Fall 2023',
            PREREQUISITES='',
            DEPARTMENT='Computer Science'
        )

        self.course.save()

        self.credentials = {
            "email": "admin@example.com",
            "password": "ad_password"
        }

        self.monkey.post("/", self.credentials, follow=True)

    def test_BadCourse(self):
        response = self.monkey.post("/section-creation/", {"sectionNumber": 901,
                                                           "courseID": '-2',
                                                           "building": 'Chemistry Building',
                                                           "roomNumber": '190',
                                                           "startTimeH": '9',
                                                           "startTimeM": '30',
                                                           "endTimeH": '10',
                                                           "endTimeM": '20'}, follow=True)
        self.assertEqual(response.context['status'], 'The course with id -2 does not exist.')

    def test_EmptyCourse(self):
        response = self.monkey.post("/section-creation/", {"sectionNumber": 901,
                                                           "courseID": '',
                                                           "building": 'Chemistry Building',
                                                           "roomNumber": '190',
                                                           "startTimeH": '9',
                                                           "startTimeM": '30',
                                                           "endTimeH": '10',
                                                           "endTimeM": '20'}, follow=True)
        self.assertEqual(str(response.context['status']), "Field 'COURSE_ID' expected a number but got ''.")

    def test_MissingInfo(self):
        response = self.monkey.post("/section-creation/", {"sectionNumber": 901,
                                                           "courseID": self.course.COURSE_ID,
                                                           "building": '',
                                                           "roomNumber": '190',
                                                           "startTimeH": '9',
                                                           "startTimeM": '30',
                                                           "endTimeH": '10',
                                                           "endTimeM": '20'}, follow=True)
        self.assertEqual(str(response.context['status']), 'Invalid building')

    def test_InvalidSection(self):
        response = self.monkey.post("/section-creation/", {"sectionNumber": '',
                                                           "courseID": self.course.COURSE_ID,
                                                           "building": 'Chemistry Building',
                                                           "roomNumber": '190',
                                                           "startTimeH": '9',
                                                           "startTimeM": '30',
                                                           "endTimeH": '10',
                                                           "endTimeM": '20'}, follow=True)
        self.assertEqual(str(response.context['status']), 'Invalid section number')

    def test_SectionCreated(self):
        response = self.monkey.post("/section-creation/", {"sectionNumber": 901,
                                                           "courseID": self.course.COURSE_ID,
                                                           "building": 'Chemistry Building',
                                                           "roomNumber": '190',
                                                           "startTimeH": '9',
                                                           "startTimeM": '30',
                                                           "endTimeH": '10',
                                                           "endTimeM": '20'}, follow=True)
        self.assertEqual(response.context['status'], 'Successfully created the section.')
