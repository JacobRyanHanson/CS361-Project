from datetime import date, time

from bs4 import BeautifulSoup
from django.test import TestCase, Client
from TA_Scheduling_App.models import Course, Section, User, CourseAssignment, SectionAssignment

class DeleteUserSuccess(TestCase):
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

        self.instructor_1 = User.objects.create(
            ROLE='INSTRUCTOR',
            FIRST_NAME='Amy',
            LAST_NAME='Smith',
            EMAIL='instructor_1@example.com',
            PHONE_NUMBER='555-987-6543',
            ADDRESS='456 Elm St',
            BIRTH_DATE=date(1995, 6, 15)
        )

        self.instructor_1.save()

        self.instructor_2 = User.objects.create(
            ROLE='INSTRUCTOR',
            FIRST_NAME='Alice',
            LAST_NAME='Smith',
            EMAIL='instructor_2@example.com',
            PHONE_NUMBER='555-987-6543',
            ADDRESS='456 Elm St',
            BIRTH_DATE=date(1995, 6, 15)
        )

        self.instructor_2.save()

        self.ta = User.objects.create(
            ROLE='TA',
            FIRST_NAME='Tim',
            LAST_NAME='Smith',
            EMAIL='ta@example.com',
            PHONE_NUMBER='555-987-6543',
            ADDRESS='456 Elm St',
            BIRTH_DATE=date(2000, 6, 15)
        )

        self.ta.save()

        self.credentials = {
            "email": "admin@example.com",
            "password": "ad_password"
        }

        self.client.post("/", self.credentials, follow=True)

        self.response = self.client.get("/user-management/", follow=True)
        self.soup = BeautifulSoup(self.response.content, 'html.parser')

        self.deletable_users = [
            {
                'ROLE': 'INSTRUCTOR',
                'FIRST_NAME': 'Amy',
                'LAST_NAME': 'Smith',
                'EMAIL': 'instructor_1@example.com',
                'PHONE_NUMBER': '555-987-6543',
                'ADDRESS': '456 Elm St',
            },
            {
                'ROLE': 'INSTRUCTOR',
                'FIRST_NAME': 'Alice',
                'LAST_NAME': 'Smith',
                'EMAIL': 'instructor_2@example.com',
                'PHONE_NUMBER': '555-987-6543',
                'ADDRESS': '456 Elm St',
            },
            {
                'ROLE': 'TA',
                'FIRST_NAME': 'Tim',
                'LAST_NAME': 'Smith',
                'EMAIL': 'ta@example.com',
                'PHONE_NUMBER': '555-987-6543',
                'ADDRESS': '456 Elm St',
            }
        ]

        # Logged-in as this user.
        self.safe_user = [
            {
                'ROLE': 'ADMIN',
                'FIRST_NAME': 'John',
                'LAST_NAME': 'Doe',
                'EMAIL': 'admin@example.com',
                'PHONE_NUMBER': '555-123-4567',
                'ADDRESS': '123 Main St',
            }
        ]

    def test_delete_users(self):
        for i, user in enumerate(self.deletable_users, 1):
            response = self.client.post("/user-management/", {'delete_user_id': i}, follow=True)
            self.assertEqual(response.context['status'], f'User with ID {i} has been deleted.')

    def test_user_count_after_deletion(self):
        initial_user_count = User.objects.count()

        for i, user in enumerate(self.deletable_users, 1):
            response = self.client.post("/user-management/", {'delete_user_id': i}, follow=True)

        # Verify that the user count has decreased by 1 after deletion
        updated_user_count = User.objects.count()
        self.assertEqual(initial_user_count - 3, updated_user_count)

    def test_other_users_not_affected_by_deletion(self):
        # Delete the user
        response = self.client.post("/user-management/", {'delete_user_id': 2}, follow=True)

        all_expected_users = self.safe_user + self.deletable_users

        for user in User.objects.all():
            user_data = {
                'ROLE': user.ROLE,
                'FIRST_NAME': user.FIRST_NAME,
                'LAST_NAME': user.LAST_NAME,
                'EMAIL': user.EMAIL,
                'PHONE_NUMBER': user.PHONE_NUMBER,
                'ADDRESS': user.ADDRESS,
            }
            self.assertIn(user_data, all_expected_users, f"User data was unexpectedly changed for user: {user_data}")

class AdminNotAbleToDeleteSelf(TestCase):
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

        self.instructor_1 = User.objects.create(
            ROLE='INSTRUCTOR',
            FIRST_NAME='Amy',
            LAST_NAME='Smith',
            EMAIL='instructor_1@example.com',
            PHONE_NUMBER='555-987-6543',
            ADDRESS='456 Elm St',
            BIRTH_DATE=date(1995, 6, 15)
        )

        self.instructor_1.save()

        self.instructor_2 = User.objects.create(
            ROLE='INSTRUCTOR',
            FIRST_NAME='Alice',
            LAST_NAME='Smith',
            EMAIL='instructor_2@example.com',
            PHONE_NUMBER='555-987-6543',
            ADDRESS='456 Elm St',
            BIRTH_DATE=date(1995, 6, 15)
        )

        self.instructor_2.save()

        self.ta = User.objects.create(
            ROLE='TA',
            FIRST_NAME='Tim',
            LAST_NAME='Smith',
            EMAIL='ta@example.com',
            PHONE_NUMBER='555-987-6543',
            ADDRESS='456 Elm St',
            BIRTH_DATE=date(2000, 6, 15)
        )

        self.ta.save()

        self.credentials = {
            "email": "admin@example.com",
            "password": "ad_password"
        }

        self.client.post("/", self.credentials, follow=True)

        self.response = self.client.get("/user-management/", follow=True)
        self.soup = BeautifulSoup(self.response.content, 'html.parser')

        self.deletable_users = [
            {
                'ROLE': 'INSTRUCTOR',
                'FIRST_NAME': 'Amy',
                'LAST_NAME': 'Smith',
                'EMAIL': 'instructor_1@example.com',
                'PHONE_NUMBER': '555-987-6543',
                'ADDRESS': '456 Elm St',
            },
            {
                'ROLE': 'INSTRUCTOR',
                'FIRST_NAME': 'Alice',
                'LAST_NAME': 'Smith',
                'EMAIL': 'instructor_2@example.com',
                'PHONE_NUMBER': '555-987-6543',
                'ADDRESS': '456 Elm St',
            },
            {
                'ROLE': 'TA',
                'FIRST_NAME': 'Tim',
                'LAST_NAME': 'Smith',
                'EMAIL': 'ta@example.com',
                'PHONE_NUMBER': '555-987-6543',
                'ADDRESS': '456 Elm St',
            }
        ]

        # Logged-in as this user.
        self.safe_user = [
            {
                'ROLE': 'ADMIN',
                'FIRST_NAME': 'John',
                'LAST_NAME': 'Doe',
                'EMAIL': 'admin@example.com',
                'PHONE_NUMBER': '555-123-4567',
                'ADDRESS': '123 Main St',
            }
        ]

    def test_admin_delete_button_disabled(self):
        # Get the user management page
        response = self.client.get("/user-management/", follow=True)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the delete button for the admin user
        admin_delete_button = soup.find('button', text='N/A')

        # Verify that the delete button exists and is disabled
        self.assertIsNotNone(admin_delete_button)
        self.assertTrue(admin_delete_button.has_attr('disabled'))

    # This is not intended functionality and is a failing case for the PBI
    def test_admin_can_delete_themselves_directly(self):
        # Send a request to delete the current admin user (who is currently logged-in)
        response = self.client.post("/user-management/", {'delete_user_id': 1}, follow=True)
        # Current expected behavior although ideally an error would be thrown.
        self.assertEqual(response.context['status'], f'User with ID 1 has been deleted.')

class TestUserDeletionSideEffects(TestCase):
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
            'course_ta_select': 'true'
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

    def test_remove_assigned_ta(self):
        # Assign TA to a course and section
        response = self.client.post("/ta-assignments/", self.course_assignment_form_data, follow=True)
        response = self.client.post("/ta-assignments/", self.section_assignment_form_data, follow=True)

        course_assignment = CourseAssignment.objects.get(TA=self.ta)
        section_assignment = SectionAssignment.objects.get(COURSE_ASSIGNMENT=course_assignment)
        self.assertIsNotNone(section_assignment)

        self.ta.delete()

        # Check if the section assignment was deleted
        with self.assertRaises(SectionAssignment.DoesNotExist):
            SectionAssignment.objects.get(COURSE_ASSIGNMENT=course_assignment)

    def test_remove_assigned_instructor(self):
        instructor_assignment_form_data = {
            'course_id': 1,
            'course_instructor': 'instructor@example.com',
        }

        # Assign instructor to course
        response = self.client.post("/ta-assignments/", instructor_assignment_form_data, follow=True)

        self.instructor.delete()

        # Check if the course instructor was set to None
        course = Course.objects.get(COURSE_ID=1)
        self.assertEqual(None, course.INSTRUCTOR)


