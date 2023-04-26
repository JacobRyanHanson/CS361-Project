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


def create_test_objects(test_case):
    test_case.user = User.objects.create(
        ROLE='INSTRUCTOR',
        FIRST_NAME='Alice',
        LAST_NAME='Smith',
        EMAIL='alice.smith@example.com',
        PASSWORD_HASH='<hashed_password>',
        PHONE_NUMBER='555-987-6543',
        ADDRESS='456 Elm St',
        BIRTH_DATE=datetime.date(1985, 6, 15)
    )
    test_case.user.save()

    test_case.course = Course.objects.create(
        COURSE_NUMBER=101,
        INSTRUCTOR=test_case.user,
        COURSE_NAME='Introduction to Computer Science',
        COURSE_DESCRIPTION='An introductory course to the world of computer science.',
        SEMESTER='Fall 2023',
        PREREQUISITES='',
        DEPARTMENT='Computer Science'
    )
    test_case.course.save()


class CreationSuccess(TestCase):
    user = None
    course = None

    def setUp(self):
        self.monkey = Client()
        login_as_admin(self.monkey)
        create_test_objects(self)

    def test_created_updates_status(self):
        response = self.monkey.post("/section-creation/", {"sectionNumber": 901,
                                                           "courseID": self.course.COURSE_ID,
                                                           "building": 'Chemistry Building',
                                                           "roomNumber": '190',
                                                           "startTimeH": '9',
                                                           "startTimeM": '30',
                                                           "endTimeH": '10',
                                                           "endTimeM": '20'}, follow=True)
        self.assertEqual(response.context['status'], 'Successfully created the section.')


class InvalidSection(TestCase):
    user = None
    course = None

    def setUp(self):
        self.monkey = Client()
        login_as_admin(self.monkey)
        create_test_objects(self)

    def test_missing_info(self):
        response = self.monkey.post("/section-creation/", {"sectionNumber": 901,
                                                           "courseID": self.course.COURSE_ID,
                                                           "building": '',
                                                           "roomNumber": '190',
                                                           "startTimeH": '9',
                                                           "startTimeM": '30',
                                                           "endTimeH": '10',
                                                           "endTimeM": '20'}, follow=True)
        self.assertEqual(str(response.context['status']), 'Invalid building')

    def test_invalid_section(self):
        response = self.monkey.post("/section-creation/", {"sectionNumber": '',
                                                           "courseID": self.course.COURSE_ID,
                                                           "building": 'Chemistry Building',
                                                           "roomNumber": '190',
                                                           "startTimeH": '9',
                                                           "startTimeM": '30',
                                                           "endTimeH": '10',
                                                           "endTimeM": '20'}, follow=True)
        self.assertEqual(str(response.context['status']), 'Invalid section number')


class InvalidAssociatedCourse(TestCase):
    user = None
    course = None

    def setUp(self):
        self.monkey = Client()
        login_as_admin(self.monkey)
        create_test_objects(self)

    def test_bad_course_id(self):
        response = self.monkey.post("/section-creation/", {"sectionNumber": 901,
                                                           "courseID": '-2',
                                                           "building": 'Chemistry Building',
                                                           "roomNumber": '190',
                                                           "startTimeH": '9',
                                                           "startTimeM": '30',
                                                           "endTimeH": '10',
                                                           "endTimeM": '20'}, follow=True)
        self.assertEqual(response.context['status'], 'The course with id -2 does not exist.')

    def test_empty_course_id(self):
        response = self.monkey.post("/section-creation/", {"sectionNumber": 901,
                                                           "courseID": '',
                                                           "building": 'Chemistry Building',
                                                           "roomNumber": '190',
                                                           "startTimeH": '9',
                                                           "startTimeM": '30',
                                                           "endTimeH": '10',
                                                           "endTimeM": '20'}, follow=True)
        self.assertEqual(str(response.context['status']), "Field 'COURSE_ID' expected a number but got ''.")
