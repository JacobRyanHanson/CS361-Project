import datetime
from datetime import date, time

from django.test import TestCase, Client
from TA_Scheduling_App.models import User, Course


class CourseCreationSuccessTest(TestCase):
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

    def test_create_course(self):
        response = self.client.post("/course-creation/", self.course_data)

        self.assertEqual(response.status_code, 200)

        courses = Course.objects.filter(COURSE_NUMBER=self.course_data["courseNumber"])
        self.assertEqual(len(courses), 1)


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

    def test_duplicate_course(self):
        self.course_data2 = {
            "courseNumber": 151,
            "instructorID": self.instructor.USER_ID,
            "courseName": 'Introduction to Computer Science',
            "courseDescription": 'An introductory course to the world of computer science.',
            "semester": 'Fall 2023',
            "prerequisites": '',
            "department": 'Computer Science'
        }

        with self.assertRaises(ValueError):
            self.course2 = Course(
                COURSE_NUMBER=self.course_data2["courseNumber"],
                INSTRUCTOR=self.instructor,
                COURSE_NAME=self.course_data2["courseName"],
                COURSE_DESCRIPTION=self.course_data2["courseDescription"],
                SEMESTER=self.course_data2["semester"],
                PREREQUISITES=self.course_data2["prerequisites"],
                DEPARTMENT=self.course_data2["department"]
            )

        response = self.client.post("/course-creation/", self.course_data2)
        self.assertEqual(response.status_code, 200)

        courses = Course.objects.filter(COURSE_NUMBER=self.course_data2["courseNumber"])
        self.assertEqual(len(courses), 1)

    def test_invalid_course_input(self):
        self.invalid_course_data = {
            "courseNumber": "$%^&*(",  # Invalid
            "instructorID": self.instructor.USER_ID,
            "courseName": 'Introduction to Computer Science',
            "courseDescription": 'An introductory course to the world of computer science.',
            "semester": 'Fall 2023',
            "prerequisites": '',
            "department": 'Computer Science'
        }
        with self.assertRaises(ValueError):
            self.invalid_course = Course(
                COURSE_NUMBER=self.invalid_course_data["courseNumber"],
                INSTRUCTOR=self.instructor,
                COURSE_NAME=self.invalid_course_data["courseName"],
                COURSE_DESCRIPTION=self.invalid_course_data["courseDescription"],
                SEMESTER=self.invalid_course_data["semester"],
                PREREQUISITES=self.invalid_course_data["prerequisites"],
                DEPARTMENT=self.invalid_course_data["department"]
            )
        response = self.client.post("/course-creation/", self.invalid_course_data)
        self.assertContains(response, "Invalid", status_code=200)




