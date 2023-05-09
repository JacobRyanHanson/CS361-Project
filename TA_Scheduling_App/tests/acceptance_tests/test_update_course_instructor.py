from datetime import date
from django.test import TestCase, Client
from TA_Scheduling_App.models import Course, User


class InstructorAssignCourseSuccess(TestCase):
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
            BIRTH_DATE=date(1990, 1, 1)
        )

        self.admin.save()

        self.instructor_1 = User(
            ROLE='INSTRUCTOR',
            FIRST_NAME='Bill',
            LAST_NAME='Doe',
            EMAIL='instructor@example.com',
            PASSWORD_HASH='bill_password',
            PHONE_NUMBER='555-222-5555',
            ADDRESS='224 Elm St',
            BIRTH_DATE=date(1990, 7, 19)
        )

        self.instructor_1.save()

        self.instructor_2 = User(
            ROLE='INSTRUCTOR',
            FIRST_NAME='Jane',
            LAST_NAME='Doe',
            EMAIL='janedoe@example.com',
            PASSWORD_HASH='jane_password',
            PHONE_NUMBER='555-242-9090',
            ADDRESS='120 College Ave',
            BIRTH_DATE=date(1988, 5, 10)
        )

        self.instructor_2.save()

        self.course_1 = Course(
            COURSE_NUMBER=151,
            COURSE_NAME='Introduction to Computer Science',
            COURSE_DESCRIPTION='An introductory course to the world of computer science.',
            SEMESTER='Fall 2023',
            PREREQUISITES='',
            DEPARTMENT='Computer Science'
        )

        self.course_1.save()

        self.course_2 = Course(
            COURSE_NUMBER=251,
            COURSE_NAME='Data Structures and Algorithms',
            COURSE_DESCRIPTION='Learning about more advanced computer science topics.',
            SEMESTER='Fall 2023',
            PREREQUISITES='',
            DEPARTMENT='Computer Science'
        )
        
        self.course_2.save()

        self.credentials = {
            "email": "admin@example.com",
            "password": "ad_password"
        }

        self.client.post("/", self.credentials, follow=True)

    def test_reassign_instructor(self):
        course_reassignment_form_data = {
            'course_id': self.course_1.COURSE_ID,
            'course_instructor_id': 2
        }

        response = self.client.post("/ta-assignments/", course_reassignment_form_data, follow=True)
        self.assertEqual(response.context['status'],
                         f'Instructor {self.instructor_1.FIRST_NAME} {self.instructor_1.LAST_NAME} assigned to course {self.course_1.COURSE_NAME}.')

    def test_assign_instructor_to_multiple_courses(self):
        course_reassignment_form_data1 = {
            'course_id': self.course_1.COURSE_ID,
            'course_instructor_id': 2
        }
        course_reassignment_form_data2 = {
            'course_id': self.course_2.COURSE_ID,
            'course_instructor_id': 2
        }

        response = self.client.post("/ta-assignments/", course_reassignment_form_data1, follow=True)
        self.assertEqual(response.context['status'],
                         f'Instructor {self.instructor_1.FIRST_NAME} {self.instructor_1.LAST_NAME} assigned to course {self.course_1.COURSE_NAME}.')

        response = self.client.post("/ta-assignments/", course_reassignment_form_data2, follow=True)
        self.assertEqual(response.context['status'],
                         f'Instructor {self.instructor_1.FIRST_NAME} {self.instructor_1.LAST_NAME} assigned to course {self.course_2.COURSE_NAME}.')


class InstructorAssignCourseFail(TestCase):
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
            BIRTH_DATE=date(1990, 1, 1)
        )

        self.admin.save()

        self.instructor = User(
            ROLE='INSTRUCTOR',
            FIRST_NAME='Bill',
            LAST_NAME='Doe',
            EMAIL='instructor@example.com',
            PASSWORD_HASH='bill_password',
            PHONE_NUMBER='555-222-5555',
            ADDRESS='224 Elm St',
            BIRTH_DATE=date(1990, 7, 19)
        )

        self.instructor.save()

        self.ta = User(
            ROLE='TA',
            FIRST_NAME='Jane',
            LAST_NAME='Doe',
            EMAIL='jdoe@example.com',
            PHONE_NUMBER='555-242-9090',
            ADDRESS='120 College Ave',
            BIRTH_DATE=date(1998, 6, 15)
        )

        self.course = Course(
            COURSE_NUMBER=151,
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

        self.client.post("/", self.credentials, follow=True)

    def test_incorrect_role(self):
        course_reassignment_form_data = {
            'course_id': self.course.COURSE_ID,
            'course_instructor_id': 1
        }

        response = self.client.post("/ta-assignments/", course_reassignment_form_data, follow=True)
        self.assertEqual(response.context['status'], f'Instructor does not exist.')

    def test_user_doesnt_exist(self):
        course_reassignment_form_data = {
            'course_id': self.course.COURSE_ID,
            'course_instructor_id': 99
        }

        response = self.client.post("/ta-assignments/", course_reassignment_form_data, follow=True)
        self.assertEqual(response.context['status'], f'Instructor does not exist.')

    def test_blank_fields(self):
        course_reassignment_form_data = {
            'course_id': '',
            'course_instructor_id': ''
        }

        response = self.client.post("/ta-assignments/", course_reassignment_form_data, follow=True)
        self.assertEqual(response.context['status'], 'An unexpected error occurred.')
        
