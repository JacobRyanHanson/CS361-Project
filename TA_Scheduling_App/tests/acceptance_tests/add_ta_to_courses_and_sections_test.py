from datetime import date, time

from django.test import TestCase, Client
from TA_Scheduling_App.models import Course, Section, User, CourseAssignment, SectionAssignment

class AddSuccess(TestCase):
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
            FIRST_NAME='Will',
            LAST_NAME='Doe',
            EMAIL='instructor@example.com',
            PASSWORD_HASH='ad_password',
            PHONE_NUMBER='555-123-4567',
            ADDRESS='123 Main St',
            BIRTH_DATE=date(1990, 1, 1)
        )

        self.instructor.save()

        self.ta = User(
            ROLE='TA',
            FIRST_NAME='Jane',
            LAST_NAME='Doe',
            EMAIL='ta@example.com',
            PHONE_NUMBER='555-987-6543',
            ADDRESS='789 Pine St',
            BIRTH_DATE=date(1998, 6, 15)
        )

        self.ta.save()

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

        self.course_assignment_form_data = {
            'course_id': 1,
            'course_ta_email': 'ta@example.com',
            'course_ta_select': True
        }

        self.section_assignment_form_data = {
            'course_id': 1,
            'section_ta_email': 'ta@example.com',
            'section_id': 1
        }

        self.credentials = {
            "email": "admin@example.com",
            "password": "ad_password"
        }

        self.client.post("/", self.credentials, follow=True)

    def test_assign_ta_to_course(self):
        response = self.client.post("/ta-assignments/", self.course_assignment_form_data, follow=True)
        self.assertEqual(response.context['status'], f'TA {self.ta.FIRST_NAME} {self.ta.LAST_NAME} assigned to course {self.course.COURSE_NAME}.')

    def test_assign_ta_to_section(self):
        response = self.client.post("/ta-assignments/", self.course_assignment_form_data, follow=True)
        response = self.client.post("/ta-assignments/", self.section_assignment_form_data, follow=True)
        self.assertEqual(response.context['status'], f'TA {self.ta.FIRST_NAME} {self.ta.LAST_NAME} assigned to section {self.section.SECTION_NUMBER}.')

    def test_assign_ta_to_multiple_courses(self):
        pass
    def test_assign_ta_to_multiple_sections(self):
        pass

