from django.test import TestCase, Client
from TA_Scheduling_App.models import Course, Section, User, SectionAssignment, CourseAssignment
from bs4 import BeautifulSoup
from datetime import date, time


def contains_text(tag, text):
    return tag.name == "option" and tag.get('title') and text in tag['title']


class ViewSkillsAdmin(TestCase):
    def setUp(self):
        self.client = Client()

        self.test_admin = User(
            ROLE='ADMIN',
            FIRST_NAME='John',
            LAST_NAME='Doe',
            EMAIL='admin@example.com',
            PASSWORD_HASH='ad_password',
            PHONE_NUMBER='555-123-4567',
            ADDRESS='123 Main St',
            BIRTH_DATE=date(1990, 1, 1)
        )

        self.test_admin.save()

        test_ta = User.objects.create(
            ROLE='TA',
            FIRST_NAME='Alice',
            LAST_NAME='Smith',
            EMAIL='alice1@example.com',
            PHONE_NUMBER='555-987-6543',
            ADDRESS='456 Elm St',
            BIRTH_DATE=date(1995, 6, 15),
            SKILLS="Java, Python, Django"
        )

        course = Course.objects.create(
            COURSE_NUMBER=151,
            COURSE_NAME='Introduction to Computer Science',
            COURSE_DESCRIPTION='An introductory course to the world of computer science.',
            SEMESTER='Fall 2023',
            PREREQUISITES='',
            DEPARTMENT='Computer Science'
        )

        section = Section.objects.create(
            SECTION_NUMBER=1,
            COURSE=course,
            BUILDING='Tech Building',
            ROOM_NUMBER='111',
            SECTION_START=time(9, 30),
            SECTION_END=time(10, 20)
        )

        self.credentials = {
            "email": "admin@example.com",
            "password": "ad_password"
        }

        self.client.post("/", self.credentials, follow=True)

        self.response = self.client.get("/ta-assignments/", follow=True)
        self.soup = BeautifulSoup(self.response.content, 'html.parser')


    def test_skills_are_visible(self):
        expected_value = 'Java, Python, Django'

        self.assertIsNotNone(self.soup.find(lambda tag: contains_text(tag, expected_value)), f"{expected_value} not found")

    def test_wrong_skills(self):
        expected_value = 'Fortran, BASIC, Standard ML'

        self.assertIsNone(self.soup.find(lambda tag: contains_text(tag, expected_value)),
                             f"{expected_value} not found")

class ViewSkillsFail(TestCase):
    def setUp(self):
        self.client = Client()

        self.test_instructor = User(
            ROLE='INSTRUCTOR',
            FIRST_NAME='John',
            LAST_NAME='Doe',
            EMAIL='instructor@example.com',
            PASSWORD_HASH='is_password',
            PHONE_NUMBER='555-123-4567',
            ADDRESS='123 Main St',
            BIRTH_DATE=date(1990, 1, 1)
        )

        self.test_instructor.save()

        test_ta = User.objects.create(
            ROLE='TA',
            FIRST_NAME='Alice',
            LAST_NAME='Smith',
            EMAIL='alice1@example.com',
            PHONE_NUMBER='555-987-6543',
            ADDRESS='456 Elm St',
            BIRTH_DATE=date(1995, 6, 15),
            SKILLS="Java, Python, Django"
        )

        course = Course.objects.create(
            COURSE_NUMBER=151,
            COURSE_NAME='Introduction to Computer Science',
            COURSE_DESCRIPTION='An introductory course to the world of computer science.',
            SEMESTER='Fall 2023',
            PREREQUISITES='',
            DEPARTMENT='Computer Science'
        )

        section = Section.objects.create(
            SECTION_NUMBER=1,
            COURSE=course,
            BUILDING='Tech Building',
            ROOM_NUMBER='111',
            SECTION_START=time(9, 30),
            SECTION_END=time(10, 20)
        )

        course_assignment = CourseAssignment.objects.create(
            COURSE=course,
            USER=self.test_instructor
        )

        self.credentials = {
            "email": "instructor@example.com",
            "password": "is_password"
        }

        self.client.post("/", self.credentials, follow=True)

        self.response = self.client.get("/ta-assignments/", follow=True)
        self.soup = BeautifulSoup(self.response.content, 'html.parser')

    def test_skills_not_visible(self):
        expected_value = 'Java, Python, Django'

        self.assertIsNone(self.soup.find(lambda tag: contains_text(tag, expected_value)),
                          f"{expected_value} shouldn't be seen by instructor")
