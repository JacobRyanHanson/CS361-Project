import datetime
from django.test import TestCase, Client

from TA_Scheduling_App.models import User, Course, Section


def login_as_admin(client: Client):
    admin = User(ROLE='ADMIN',
                 FIRST_NAME='John',
                 LAST_NAME='Doe',
                 EMAIL='admin@example.com',
                 PASSWORD_HASH='ad_password',
                 PHONE_NUMBER='555-123-4567',
                 ADDRESS='123 Main St',
                 BIRTH_DATE=datetime.date(1990, 1, 1))

    admin.save()

    client.post("/", {
        "email": admin.EMAIL,
        "password": admin.PASSWORD_HASH
    })


class CreationSuccess(TestCase):
    user = None
    course = None

    def setUp(self):
        self.client = Client()
        login_as_admin(self.client)

        self.course = Course.objects.create(
            COURSE_NUMBER=101,
            COURSE_NAME='Introduction to Computer Science',
            COURSE_DESCRIPTION='An introductory course to the world of computer science.',
            SEMESTER='Fall 2023',
            PREREQUISITES='',
            DEPARTMENT='Computer Science'
        )

        self.section_form_data = {
            "section_type": "LAB",
            "section_number": 901,
            "course_id": self.course.COURSE_ID,
            "building": 'Chemistry Building',
            "room_number": '190',
            "start_time": '13:00',
            "end_time": '14:00',
        }

    def test_created_updates_status(self):
        response = self.client.post("/section-creation/", self.section_form_data, follow=True)
        self.assertEqual(response.context['status'], 'Successfully created the section.')

    def test_created_updates_database(self):
        self.client.post("/section-creation/", self.section_form_data, follow=True)
        section = Section.objects.get(SECTION_NUMBER=901)
        self.assertEqual(section.COURSE_id, self.course.COURSE_ID)


class InvalidSection(TestCase):
    user = None
    course = None

    def setUp(self):
        self.client = Client()
        login_as_admin(self.client)

        self.course = Course.objects.create(
            COURSE_NUMBER=101,
            COURSE_NAME='Introduction to Computer Science',
            COURSE_DESCRIPTION='An introductory course to the world of computer science.',
            SEMESTER='Fall 2023',
            PREREQUISITES='',
            DEPARTMENT='Computer Science'
        )

        self.section_form_data = {
            "section_type": "LAB",
            "section_number": 901,
            "course_id": self.course.COURSE_ID,
            "building": 'Chemistry Building',
            "room_number": '190',
            "start_time": '13:00',
            "end_time": '14:00',
        }

    def test_missing_info(self):
        self.section_form_data['building'] = ""
        response = self.client.post("/section-creation/", self.section_form_data, follow=True)
        self.assertEqual(str(response.context['status']), 'Invalid building.')

    def test_invalid_section(self):
        self.section_form_data['section_number'] = ""
        response = self.client.post("/section-creation/", self.section_form_data, follow=True)
        self.assertEqual(str(response.context['status']), 'Invalid section number.')


class InvalidAssociatedCourse(TestCase):
    user = None
    course = None

    def setUp(self):
        self.client = Client()
        login_as_admin(self.client)

        self.course = Course.objects.create(
            COURSE_NUMBER=101,
            COURSE_NAME='Introduction to Computer Science',
            COURSE_DESCRIPTION='An introductory course to the world of computer science.',
            SEMESTER='Fall 2023',
            PREREQUISITES='',
            DEPARTMENT='Computer Science'
        )

        self.section_form_data = {
            "section_type": "LAB",
            "section_number": 901,
            "course_id": self.course.COURSE_ID,
            "building": 'Chemistry Building',
            "room_number": '190',
            "start_time": '13:00',
            "end_time": '14:00',
        }

    def test_bad_course_id(self):
        self.section_form_data['course_id'] = "-2"
        response = self.client.post("/section-creation/", self.section_form_data, follow=True)
        self.assertEqual(response.context['status'], 'The course does not exist.')

    def test_empty_course_id(self):
        self.section_form_data['course_id'] = ""
        response = self.client.post("/section-creation/", self.section_form_data, follow=True)
        self.assertEqual(str(response.context['status']), "Field 'COURSE_ID' expected a number but got ''.")
