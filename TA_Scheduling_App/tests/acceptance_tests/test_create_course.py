import datetime
from datetime import date, time

from django.test import TestCase, Client
from TA_Scheduling_App.models import User, Course


class AddCourseTestSuccess(TestCase):
    def setUp(self):
        self.client = Client()

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

        self.instructor = User(
            ROLE='INSTRUCTOR',
            FIRST_NAME='Will',
            LAST_NAME='Doe',
            EMAIL='instructor@example.com',
            PASSWORD_HASH='ad_password',
            PHONE_NUMBER='555-123-4567',
            ADDRESS='123 Main St',
            BIRTH_DATE=date(1990, 1, 1)
        )

        self.instructor.save()

        self.course_form_data = {
            "course_number": 151,
            "instructor_id": 2,
            "course_name": 'Introduction to Computer Science',
            "course_description": 'An introductory course to the world of computer science.',
            "semester": 'Fall 2023',
            "prerequisites": '',
            "department": 'Computer Science'
        }

        # Log the user in
        self.credentials = {
            "email": "admin@example.com",
            "password": "ad_password"
        }

        self.client.post("/", self.credentials, follow=True)

    def test_create_course_in_system(self):
        self.client.post("/course-creation/", self.course_form_data, follow=True)
        self.assertEqual(len(Course.objects.filter(COURSE_NUMBER=self.course_form_data["course_number"])), 1)

    def test_success_message_displayed(self):
        response = self.client.post("/course-creation/", self.course_form_data, follow=True)
        self.assertEqual(str(response.context['status']), f'Successfully created course { self.course_form_data["course_name"]}.')


class InvalidInputTest(TestCase):
    def setUp(self):
        self.client = Client()

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

        self.instructor = User(
            ROLE='INSTRUCTOR',
            FIRST_NAME='Will',
            LAST_NAME='Doe',
            EMAIL='instructor@example.com',
            PASSWORD_HASH='ad_password',
            PHONE_NUMBER='555-123-4567',
            ADDRESS='123 Main St',
            BIRTH_DATE=date(1990, 1, 1)
        )

        self.instructor.save()

        self.course_form_data = {
            "course_number": '113',
            "instructor_id": self.instructor.USER_ID,
            "course_name": 'Introduction to Computer Science',
            "course_description": 'An introductory course to the world of computer science.',
            "semester": 'Fall 2023',
            "prerequisites": '',
            "department": 'Computer Science'
        }

        # Log the user in
        self.credentials = {
            "email": "admin@example.com",
            "password": "ad_password"
        }
        self.client.post("/", self.credentials, follow=True)

    def test_invalid_blank(self):
        # Input fields are blank, but they are required (should not be possible)
        invalid_course_data = {
            "course_number": " ",
            "instructor_id": " ",
            "course_name": '',
            "course_description": '',
            "semester": '',
            "prerequisites": '',
            "department": ''
        }

        response = self.client.post("/course-creation/", invalid_course_data, follow=True)
        self.assertEqual(str(response.context['status']), "Invalid course number.")

    def test_invalid_course_number(self):
        self.course_form_data['course_number'] = "$%^&*("
        response = self.client.post("/course-creation/", self.course_form_data, follow=True)
        self.assertEqual(str(response.context['status']), 'Invalid course number.')

    def test_invalid_course_name(self):
        self.course_form_data['course_name'] = " _)(* & COMP"
        response = self.client.post("/course-creation/", self.course_form_data, follow=True)
        self.assertEqual(str(response.context['status']), 'Invalid course name.')

    def test_invalid_course_Description(self):
        self.course_form_data['course_description'] = '46880An introd%^uctory cou%&**rse to the world of computer science.'
        response = self.client.post("/course-creation/", self.course_form_data, follow=True)
        self.assertEqual(str(response.context['status']), 'Invalid course description.')

    def test_invalid_course_semester(self):
        self.course_form_data['semester'] = "!aaaaaaa!"
        response = self.client.post("/course-creation/",  self.course_form_data, follow=True)
        self.assertEqual(str(response.context['status']), 'Invalid semester.')

    def test_invalid_course_prerequisites(self):
        self.course_form_data['prerequisites'] = "4444"
        response = self.client.post("/course-creation/", self.course_form_data, follow=True)
        self.assertEqual(str(response.context['status']), 'Invalid prerequisites.')

    def test_invalid_course_department(self):
        self.course_form_data['department'] = "C0mputer Science"
        response = self.client.post("/course-creation/", self.course_form_data, follow=True)
        self.assertEqual(str(response.context['status']), 'Invalid department.')


class DuplicateCreationFailTest(TestCase):
    def setUp(self):
        self.client = Client()

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

        self.instructor = User(
            ROLE='INSTRUCTOR',
            FIRST_NAME='Will',
            LAST_NAME='Doe',
            EMAIL='instructor@example.com',
            PASSWORD_HASH='ad_password',
            PHONE_NUMBER='555-123-4567',
            ADDRESS='123 Main St',
            BIRTH_DATE=date(1990, 1, 1)
        )

        self.instructor.save()

        self.course = Course(
            COURSE_NUMBER=151,
            COURSE_NAME='Introduction to Computer Science',
            COURSE_DESCRIPTION='An introductory course to the world of computer science.',
            SEMESTER='Fall 2023',
            PREREQUISITES='',
            DEPARTMENT='Computer Science'
        )

        self.course.save()

        self.course_data = {
            "courseNumber": 151,
            "instructorID": self.instructor.USER_ID,
            "courseName": 'Introduction to Computer Science',
            "courseDescription": 'An introductory course to the world of computer science.',
            "semester": 'Fall 2023',
            "prerequisites": '',
            "department": 'Computer Science'
        }

        # Log the user in
        self.credentials = {
            "email": "admin@example.com",
            "password": "ad_password"
        }
        self.client.post("/", self.credentials, follow=True)

    def test_duplicate_course_display_message(self):
        course_data_2 = {
            "course_number": 151,
            "instructor_id": self.instructor.USER_ID,
            "course_name": 'Introduction to Computer Science',
            "course_description": 'An introductory course to the world of computer science.',
            "semester": 'Fall 2023',
            "prerequisites": '',
            "department": 'Computer Science'
        }

        response = self.client.post("/course-creation/", course_data_2, follow=True)
        self.assertEqual(str(response.context['status']), "Duplicate course number assignment failed.")

    def test_duplicate_course_not_in_system(self):
        self.course_data_2 = {
            "courseNumber": 151,
            "instructorID": self.instructor.USER_ID,
            "courseName": 'Introduction to Computer Science',
            "courseDescription": 'An introductory course to the world of computer science.',
            "semester": 'Fall 2023',
            "prerequisites": '',
            "department": 'Computer Science'
        }

        self.assertEqual(len(Course.objects.filter(COURSE_NUMBER=self.course_data_2["courseNumber"])), 1)
