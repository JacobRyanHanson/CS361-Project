from datetime import date, time

from django.test import TestCase, Client
from TA_Scheduling_App.models import Course, Section, User, CourseAssignment

class AddTASuccess(TestCase):
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
            COURSE_NAME='Introduction to Computer Science',
            COURSE_DESCRIPTION='An introductory course to the world of computer science.',
            SEMESTER='Fall 2023',
            PREREQUISITES='',
            DEPARTMENT='Computer Science'
        )

        self.course.save()

        self.section = Section(
            SECTION_TYPE="LAB",
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
            'course_ta_id': 3,
            'course_ta_grader_status': 'True'
        }

        self.section_assignment_form_data = {
            'course_id': 1,
            'section_id': 1,
            'section_ta_id': 3
        }

        self.other_course = Course(
            COURSE_NUMBER=178,
            COURSE_NAME='New Introduction to Computer Science',
            COURSE_DESCRIPTION='An introductory course to the world of computer science.',
            SEMESTER='Fall 2023',
            PREREQUISITES='',
            DEPARTMENT='Computer Science'
        )

        self.other_course.save()

        self.other_section = Section(
            SECTION_TYPE="LAB",
            SECTION_NUMBER=76,
            COURSE=self.course,
            BUILDING='Tech Building',
            ROOM_NUMBER='111',
            SECTION_START=time(9, 30),
            SECTION_END=time(10, 20)
        )

        self.other_section.save()

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
        self.assertEqual(response.context['status'], f'TA {self.ta.FIRST_NAME} {self.ta.LAST_NAME} assigned to section.')

    def test_assign_ta_to_multiple_courses(self):
        response = self.client.post("/ta-assignments/", self.course_assignment_form_data, follow=True)

        other_course_assignment_form_data = {
            'course_id': 2,
            'course_ta_id': 3,
            'course_ta_grader_status': 'True'
        }

        response = self.client.post("/ta-assignments/", other_course_assignment_form_data, follow=True)
        self.assertEqual(response.context['status'], f'TA {self.ta.FIRST_NAME} {self.ta.LAST_NAME} assigned to course {self.other_course.COURSE_NAME}.')

    def test_assign_ta_to_multiple_sections(self):
        response = self.client.post("/ta-assignments/", self.course_assignment_form_data, follow=True)
        response = self.client.post("/ta-assignments/", self.section_assignment_form_data, follow=True)

        other_section_assignment_form_data = {
            'course_id': 1,
            'section_id': 2,
            'section_ta_id': 3
        }

        response = self.client.post("/ta-assignments/", other_section_assignment_form_data, follow=True)
        self.assertEqual(response.context['status'], f'TA {self.ta.FIRST_NAME} {self.ta.LAST_NAME} assigned to section.')


class AddTAWithBadInput(TestCase):
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
            COURSE_NAME='Introduction to Computer Science',
            COURSE_DESCRIPTION='An introductory course to the world of computer science.',
            SEMESTER='Fall 2023',
            PREREQUISITES='',
            DEPARTMENT='Computer Science'
        )

        self.course.save()

        self.section = Section(
            SECTION_TYPE="LAB",
            SECTION_NUMBER=1,
            COURSE=self.course,
            BUILDING='Tech Building',
            ROOM_NUMBER='111',
            SECTION_START=time(9, 30),
            SECTION_END=time(10, 20)
        )

        self.section.save()

        self.invalid_ta_course_form_data = {
            'course_id': 1,
            'course_ta_id': -1,
            'course_ta_grader_status': 'True'
        }

        self.credentials = {
            "email": "admin@example.com",
            "password": "ad_password"
        }

        self.client.post("/", self.credentials, follow=True)

    def test_blank_fields(self):
        blank_form_data = {
            'course_id': '',
            'course_ta_id': '',
            'course_ta_grader_status': 'True'
        }

        response = self.client.post("/ta-assignments/", blank_form_data, follow=True)
        # Input fields are blank, but they are required (should not be possible)
        self.assertEqual(response.context['status'], "An unexpected error occurred.")

    def test_invalid_ta_email_for_course_assignment(self):
        response = self.client.post("/ta-assignments/", self.invalid_ta_course_form_data, follow=True)
        self.assertEqual(response.context['status'], f'TA does not exist.')

    def test_invalid_ta_email_for_section_assignment(self):
        invalid_ta_section_form_data = {
            'course_id': 1,
            'section_id': 1,
            'section_ta_id': -1
        }

        response = self.client.post("/ta-assignments/", self.invalid_ta_course_form_data, follow=True)
        response = self.client.post("/ta-assignments/", invalid_ta_section_form_data, follow=True)
        self.assertEqual(response.context['status'], f'TA does not exist.')

    def test_invalid_ta_grader_status(self):
        invalid_ta_section_form_data = {
            'course_id': 1,
            'course_ta_id': 3,
            'course_ta_grader_status': "aaaa"
        }

        response = self.client.post("/ta-assignments/", invalid_ta_section_form_data, follow=True)
        # Allow assignment but set grader status to false.
        self.assertEqual(response.context['status'], f'TA {self.ta.FIRST_NAME} {self.ta.LAST_NAME} assigned to course {self.course.COURSE_NAME}.')
        self.assertEqual(False, CourseAssignment.objects.get(USER=self.ta).IS_GRADER)


class InvalidSectionAssignment(TestCase):
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
            COURSE_NAME='Introduction to Computer Science',
            COURSE_DESCRIPTION='An introductory course to the world of computer science.',
            SEMESTER='Fall 2023',
            PREREQUISITES='',
            DEPARTMENT='Computer Science'
        )

        self.course.save()

        self.other_course = Course(
            COURSE_NUMBER=760,
            COURSE_NAME='Introduction to Computer Science',
            COURSE_DESCRIPTION='An introductory course to the world of computer science.',
            SEMESTER='Fall 2023',
            PREREQUISITES='',
            DEPARTMENT='Science'
        )

        self.other_course.save()

        self.section = Section(
            SECTION_TYPE="LAB",
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
            'course_ta_id': 3,
            'course_ta_grader_status': 'True'
        }

        self.other_course_assignment_form_data = {
            'course_id': 2,
            'course_ta_id': 3,
            'course_ta_grader_status': 'True'
        }

        self.section_assignment_form_data = {
            'course_id': 1,
            'section_id': 1,
            'section_ta_id': 3,
        }

        self.credentials = {
            "email": "admin@example.com",
            "password": "ad_password"
        }

        self.client.post("/", self.credentials, follow=True)

    def test_assign_ta_to_unrelated_section_no_assigned_course(self):
        response = self.client.post("/ta-assignments/", self.section_assignment_form_data, follow=True)
        self.assertEqual(response.context['status'], f'The TA is not assigned to the course.')

    def test_assign_ta_to_unrelated_section_wrong_course(self):
        # Assign TA to a course.
        response = self.client.post("/ta-assignments/", self.other_course_assignment_form_data, follow=True)
        # Attempt to assign TA to a section on a different course.
        response = self.client.post("/ta-assignments/", self.section_assignment_form_data, follow=True)
        self.assertEqual(response.context['status'], f'The TA is not assigned to the course.')

    def test_assign_ta_to_unrelated_section_and_section_does_not_exist(self):
        section_assignment_form_data = {
            'course_id': 1,
            'section_id': 99,
            'section_ta_id': 3,
        }

        response = self.client.post("/ta-assignments/", self.course_assignment_form_data, follow=True)
        response = self.client.post("/ta-assignments/", section_assignment_form_data, follow=True)
        self.assertEqual(response.context['status'], f'Section does not exist.')

class InvalidDuplicateAssignment(TestCase):
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
            COURSE_NAME='Introduction to Computer Science',
            COURSE_DESCRIPTION='An introductory course to the world of computer science.',
            SEMESTER='Fall 2023',
            PREREQUISITES='',
            DEPARTMENT='Computer Science'
        )

        self.course.save()

        self.section = Section(
            SECTION_TYPE="LAB",
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
            'course_ta_id': 3,
            'course_ta_grader_status': 'True'
        }

        self.section_assignment_form_data = {
            'course_id': 1,
            'section_id': 1,
            'section_ta_id': 3,
        }

        self.credentials = {
            "email": "admin@example.com",
            "password": "ad_password"
        }

        self.client.post("/", self.credentials, follow=True)

    def test_duplicate_ta_assignment_to_course(self):
        response = self.client.post("/ta-assignments/", self.course_assignment_form_data, follow=True)
        response = self.client.post("/ta-assignments/", self.course_assignment_form_data, follow=True)
        self.assertEqual(str(response.context['status']), "Duplicate assignment of user to course failed.")

    def test_duplicate_ta_assignment_to_section(self):
        response = self.client.post("/ta-assignments/", self.course_assignment_form_data, follow=True)
        # Duplicate section assignments
        response = self.client.post("/ta-assignments/", self.section_assignment_form_data, follow=True)
        response = self.client.post("/ta-assignments/", self.section_assignment_form_data, follow=True)
        self.assertEqual(str(response.context['status']), "Duplicate assignment of user to section failed.")




