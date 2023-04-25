import datetime
from datetime import date, time

from django.test import TestCase, Client
from TA_Scheduling_App.models import User, Course


class DeleteCourseSuccessTest(TestCase):
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

        # Log the user in
        self.credentials = {
            "email": "admin@example.com",
            "password": "ad_password"
        }
        self.client.post("/", self.credentials, follow=True)

    def test_delete_course(self):
        courses = Course.objects.filter(COURSE_NUMBER=self.course.COURSE_NUMBER)
        self.assertEqual(len(courses), 1)

        response = self.client.post("/ta-assignments/", {"courseNumber": self.course.delete()})
        self.assertEqual(response.status_code, 200)

        courses = Course.objects.filter(COURSE_NUMBER=self.course.COURSE_NUMBER)
        self.assertEqual(len(courses), 0)


class CourseCreationFailTest(TestCase):
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

        self.newCourse = Course(
            COURSE_NUMBER=300,
            INSTRUCTOR=self.instructor,
            COURSE_NAME='Intermediate Computer Programming',
            COURSE_DESCRIPTION='An intermediate course.',
            SEMESTER='Fall 2023',
            PREREQUISITES='',
            DEPARTMENT='Computer Science'
        )

        self.newCourse.save()

        # Log the user in
        self.credentials = {
            "email": "admin@example.com",
            "password": "ad_password"
        }
        self.client.post("/", self.credentials, follow=True)

    def test_delete_nonexistent_course(self):
        courses = Course.objects.filter(COURSE_NUMBER=self.course.COURSE_NUMBER)
        self.assertEqual(len(courses), 1)

        response = self.client.post("/ta-assignments/", {"courseNumber": self.course.delete()})
        self.assertEqual(response.status_code, 200)

        courses = Course.objects.filter(COURSE_NUMBER=self.course.COURSE_NUMBER)
        self.assertEqual(len(courses), 0)

        with self.assertRaises(ValueError):
            # Attempt to delete course that doesn't exist
            response = self.client.post("/ta-assignments/", {"courseNumber": self.course.delete()})
            self.assertContains(response, "does not exist", status_code=200)

        # Test that newCourse has not been deleted
        courses = Course.objects.filter(COURSE_NUMBER=self.newCourse.COURSE_NUMBER)
        self.assertEqual(len(courses), 1)
