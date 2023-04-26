import datetime
from datetime import date, time

from django.test import TestCase, Client
from TA_Scheduling_App.models import User, Course, Section


class DeleteSectionSuccessTest(TestCase):
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
            INSTRUCTOR=self.instructor,
            COURSE_NAME='Introduction to Computer Science',
            COURSE_DESCRIPTION='An introductory course to the world of computer science.',
            SEMESTER='Fall 2023',
            PREREQUISITES='',
            DEPARTMENT='Computer Science'
        )

        self.course.save()

        self.section = Section(
            SECTION_NUMBER=1,
            COURSE=self.course,
            BUILDING='Tech Building',
            ROOM_NUMBER='111',
            SECTION_START=time(9, 30),
            SECTION_END=time(10, 20)
        )

        self.section.save()

        # Log the user in
        self.credentials = {
            "email": "admin@example.com",
            "password": "ad_password"
        }
        self.client.post("/", self.credentials, follow=True)

    def test_delete_section(self):
        self.assertEqual(len(Section.objects.filter(SECTION_NUMBER=self.section.SECTION_NUMBER)), 1)

        response = self.client.post("/ta-assignments/", {"sectionNumber": self.section.delete()})
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(Section.objects.filter(SECTION_NUMBER=self.section.SECTION_NUMBER)), 0)

    def test_delete_section_removes_assignments(self):
        # Need to complete
        pass


class DeleteSectionFailTest(TestCase):
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
            INSTRUCTOR=self.instructor,
            COURSE_NAME='Introduction to Computer Science',
            COURSE_DESCRIPTION='An introductory course to the world of computer science.',
            SEMESTER='Fall 2023',
            PREREQUISITES='',
            DEPARTMENT='Computer Science'
        )

        self.course.save()

        self.section = Section(
            SECTION_NUMBER=1,
            COURSE=self.course,
            BUILDING='Tech Building',
            ROOM_NUMBER='111',
            SECTION_START=time(9, 30),
            SECTION_END=time(10, 20)
        )

        self.section.save()

        self.newSection = Section(
            SECTION_NUMBER=7,
            COURSE=self.course,
            BUILDING='Tech Building',
            ROOM_NUMBER='555',
            SECTION_START=time(9, 30),
            SECTION_END=time(10, 20)
        )

        self.newSection.save()

        # Log the user in
        self.credentials = {
            "email": "admin@example.com",
            "password": "ad_password"
        }
        self.client.post("/", self.credentials, follow=True)

    def test_delete_nonexistent_section(self):
        self.assertEqual(len(Section.objects.filter(SECTION_NUMBER=self.section.SECTION_NUMBER)), 1)

        response = self.client.post("/ta-assignments/", {"sectionNumber": self.section.delete()})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Section.objects.filter(SECTION_NUMBER=self.section.SECTION_NUMBER)), 0)

        with self.assertRaises(ValueError):
            # Attempt to delete section that doesn't exist
            self.client.post("/ta-assignments/", {"sectionNumber": self.section.delete()})
            self.assertEqual(response, 'Section does not exist.')

        # Test that newSection has not been deleted
        self.assertEqual(len(Section.objects.filter(SECTION_NUMBER=self.newSection.SECTION_NUMBER)), 1)
