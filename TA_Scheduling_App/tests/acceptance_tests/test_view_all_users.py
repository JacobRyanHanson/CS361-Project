from datetime import date, time

from bs4 import BeautifulSoup
from django.test import TestCase, Client
from TA_Scheduling_App.models import Course, Section, User


def contains_text(tag, text):
    return tag.string is not None and text.strip() in tag.string.strip()


class ViewAllSuccess(TestCase):
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

        self.expected_users = [
            {
                'ROLE': 'ADMIN',
                'FIRST_NAME': 'John',
                'LAST_NAME': 'Doe',
                'EMAIL': 'admin@example.com',
                'PHONE_NUMBER': '555-123-4567',
                'ADDRESS': '123 Main St',
            },
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

    def test_all_users_are_visible(self):
        for user in self.expected_users:
            for key, value in user.items():
                self.assertIsNotNone(self.soup.find(lambda tag: contains_text(tag, value)), f"{key} {value} not found")

    def test_no_extra_users_exist(self):
        # Check for any unexpected users
        for user in User.objects.all():
            user_data = {
                'ROLE': user.ROLE,
                'FIRST_NAME': user.FIRST_NAME,
                'LAST_NAME': user.LAST_NAME,
                'EMAIL': user.EMAIL,
                'PHONE_NUMBER': user.PHONE_NUMBER,
                'ADDRESS': user.ADDRESS,
            }
            self.assertIn(user_data, self.expected_users, f"Unexpected user found: {user_data}")


class ViewAllFail(TestCase):
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

        self.expected_users = [
            {
                'ROLE': 'ADMIN',
                'FIRST_NAME': 'John',
                'LAST_NAME': 'Doe',
                'EMAIL': 'admin@example.com',
                'PHONE_NUMBER': '555-123-4567',
                'ADDRESS': '123 Main St',
            },
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

    def test_no_users_in_system_and_none_visible(self):
        users = User.objects.all()

        if len(users) == 1:  # Only the admin user exists
            self.assertIsNone(self.soup.find(lambda tag: tag.name == "h5" and contains_text(tag, "User")),
                              "A user was found")

    def test_user_not_visible_when_deleted(self):
        self.admin.delete()
        self.instructor_1.delete()
        self.instructor_2.delete()
        self.ta.delete()

        self.response = self.client.get("/user-management/", follow=True)
        self.soup = BeautifulSoup(self.response.content, 'html.parser')

        for user in self.expected_users:
            self.assertIsNone(self.soup.find(lambda tag: contains_text(tag, user['FIRST_NAME'])),
                              "Deleted user was found")
