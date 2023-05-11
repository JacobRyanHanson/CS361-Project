from datetime import date, time

from bs4 import BeautifulSoup
from django.test import TestCase, Client
from TA_Scheduling_App.models import User, Course, Section, CourseAssignment, SectionAssignment


def contains_text(tag, text):
    return tag.string is not None and text.strip() in tag.string.strip()


class InstructorAssignTASuccess(TestCase):
    def setUp(self):
        self.client = Client()

        self.instructor = User(
            ROLE='INSTRUCTOR',
            FIRST_NAME='John',
            LAST_NAME='Doe',
            EMAIL='instructor@example.com',
            PASSWORD_HASH='instructor_password',
            PHONE_NUMBER='555-123-4567',
            ADDRESS='1234 Elm St',
            BIRTH_DATE=date(1970, 1, 1)
        )

        self.instructor.save()

        self.credentials = {
            "email": "instructor@example.com",
            "password": "instructor_password"
        }

        self.course = Course.objects.create(
            COURSE_NUMBER=648,
            COURSE_NAME='Test Course',
            COURSE_DESCRIPTION='A test course.',
            SEMESTER='Fall 2023',
            PREREQUISITES='',
            DEPARTMENT='Computer Science'
        )

        self.course.save()

        self.section = Section.objects.create(
            SECTION_TYPE="LECTURE",
            SECTION_NUMBER=894,
            COURSE=self.course,
            BUILDING='Tech Building',
            ROOM_NUMBER='999',
            SECTION_START=time(9, 30),
            SECTION_END=time(10, 20)
        )

        self.section.save()

        self.instructor_course_assignment = CourseAssignment.objects.create(
            COURSE=self.course,
            USER=self.instructor
        )

        self.instructor_course_assignment.save()

        self.section_assignment_form_data = {
            'course_id': 1,
            'section_id': 1,
            'section_instructor_id': 1,
        }

        # Login as an instructor.
        self.client.post("/", self.credentials, follow=True)

    def test_check_instructor_in_dropdown(self):
        response = self.client.get("/ta-assignments/", follow=True)
        self.client.post("/ta-assignments/", self.section_assignment_form_data, follow=True)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertIsNotNone(
            soup.find(lambda tag: contains_text(tag, f'{self.instructor.FIRST_NAME} {self.instructor.LAST_NAME}')),
            f'{self.instructor.FIRST_NAME} {self.instructor.LAST_NAME} not found')

    def test_assign_instructor_to_section(self):
        response = self.client.post("/ta-assignments/", self.section_assignment_form_data, follow=True)
        self.assertEqual(str(response.context['status']),
                         f'Instructor {self.instructor.FIRST_NAME} {self.instructor.LAST_NAME} assigned to section.')

    def test_instructor_assignment_exists_in_db(self):
        response = self.client.post("/ta-assignments/", self.section_assignment_form_data, follow=True)

        instructor_assignment = SectionAssignment.objects.filter(
            COURSE_ASSIGNMENT=self.instructor_course_assignment,
            SECTION=self.section
        )

        self.assertTrue(instructor_assignment.exists() and len(instructor_assignment) == 1)


class InstructorAssignImpossibleTA(TestCase):
    def setUp(self):
        self.client = Client()

        self.instructor = User(
            ROLE='INSTRUCTOR',
            FIRST_NAME='John',
            LAST_NAME='Doe',
            EMAIL='instructor@example.com',
            PASSWORD_HASH='instructor_password',
            PHONE_NUMBER='555-123-4567',
            ADDRESS='1234 Elm St',
            BIRTH_DATE=date(1970, 1, 1)
        )

        self.instructor.save()

        self.credentials = {
            "email": "instructor@example.com",
            "password": "instructor_password"
        }

        self.course = Course.objects.create(
            COURSE_NUMBER=648,
            COURSE_NAME='Test Course',
            COURSE_DESCRIPTION='A test course.',
            SEMESTER='Fall 2023',
            PREREQUISITES='',
            DEPARTMENT='Computer Science'
        )

        self.course.save()

        self.section = Section.objects.create(
            SECTION_TYPE="LECTURE",
            SECTION_NUMBER=894,
            COURSE=self.course,
            BUILDING='Tech Building',
            ROOM_NUMBER='999',
            SECTION_START=time(9, 30),
            SECTION_END=time(10, 20)
        )

        self.section.save()

        self.instructor_course_assignment = CourseAssignment.objects.create(
            COURSE=self.course,
            USER=self.instructor
        )

        self.instructor_course_assignment.save()

        self.section_assignment_form_data = {
            'course_id': 1,
            'section_id': 1,
            'section_instructor_id': "None",
        }

        # Login as an instructor.
        self.client.post("/", self.credentials, follow=True)

    # Shouldn't be possible
    def test_update_instructor_with_none(self):
        response = self.client.post("/ta-assignments/", self.section_assignment_form_data, follow=True)
        self.assertEqual(str(response.context['status']), f'')


    def test_no_new_instructor_assignments_created(self):
        nonexistent_instructor_id = 999
        self.section_assignment_form_data['section_instructor_id'] = nonexistent_instructor_id
        response = self.client.post("/ta-assignments/", self.section_assignment_form_data, follow=True)
        all_instructor_assignments = SectionAssignment.objects.filter(
            COURSE_ASSIGNMENT__USER__USER_ID=nonexistent_instructor_id,
            SECTION=self.section
        )

        self.assertFalse(all_instructor_assignments.exists())
