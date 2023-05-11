import datetime
import django.urls

from bs4 import BeautifulSoup, ResultSet
from django.test import TestCase, Client
from TA_Scheduling_App.models import User


def contains_text(tag, text):
    return tag.string is not None and text.strip() in tag.string.strip()

def login_user(client: Client, user):
    credentials = {
        "email": user.EMAIL,
        "password": user.PASSWORD_HASH
    }
    client.post("/", credentials, follow=True)


class LoadFailNoAuth(TestCase):
    def setUp(self):
        self.client = Client()

    def test_noauth_get_redirects(self):
        # if a user is not logged in, are they directed to log in before viewing this page?
        response = self.client.get("/account-settings/", follow=True)
        self.assertRedirects(response, "/")

    def test_noauth_post_rejects(self):
        # if a user is not logged in, this is an illegal attempt to modify info!
        # content of request does not matter.
        response = self.client.post("/account-settings/", None, follow=True)
        self.assertEqual(response.status_code, 403)


class LoadSuccess(TestCase):
    def setUp(self):
        self.client = Client()

        self.ta = User(ROLE='TA',
                       FIRST_NAME='Jane',
                       LAST_NAME='Doe',
                       EMAIL='test@example.com',
                       PASSWORD_HASH='test_password',
                       PHONE_NUMBER='555-123-4567',
                       ADDRESS='1234 Elm St',
                       BIRTH_DATE=datetime.date(1995, 8, 30))

        self.ta.save()

        self.ta_form_data = {
            "first_name": self.ta.FIRST_NAME,
            "last_name": self.ta.LAST_NAME,
            "email": self.ta.EMAIL,
            "phone_number": self.ta.PHONE_NUMBER,
            "address": self.ta.ADDRESS,
            "birth_date": self.ta.BIRTH_DATE.isoformat(),
            "skills": ""
        }

        login_user(self.client, self.ta)

        self.response = self.client.get("/account-settings/", follow=True)

        self.soup = BeautifulSoup(self.response.content, 'html.parser')

    def test_auth_success(self):
        # is the account settings page viewable for a logged in user?
        self.assertEqual(self.response.status_code, 200)

    def test_template_renders(self):
        self.assertTemplateUsed(self.response, "account-settings.html")

    def test_form_prefilled(self):
        for key, value in self.ta_form_data.items():
            if key is not "skills":
                self.assertIsNotNone(self.soup.find('input', {'value': value}), f"{key} {value} not found")


class UpdateFail(TestCase):
    def setUp(self):
        self.client = Client()

        self.ta = User(ROLE='TA',
                       FIRST_NAME='Jane',
                       LAST_NAME='Doe',
                       EMAIL='test@example.com',
                       PASSWORD_HASH='test_password',
                       PHONE_NUMBER='555-123-4567',
                       ADDRESS='1234 Elm St',
                       BIRTH_DATE=datetime.date(1995, 8, 30))

        self.ta.save()

        self.ta_form_data = {
            "first_name": self.ta.FIRST_NAME,
            "last_name": self.ta.LAST_NAME,
            "email": self.ta.EMAIL,
            "phone_number": self.ta.PHONE_NUMBER,
            "address": self.ta.ADDRESS,
            "birth_date": self.ta.BIRTH_DATE.isoformat(),
            "skills": ""
        }

        login_user(self.client, self.ta)

        self.response = self.client.get("/account-settings/", follow=True)

        self.soup = BeautifulSoup(self.response.content, 'html.parser')

    def test_invalid_first_name(self):
        self.ta_form_data["first_name"] = "1234"
        response = self.client.post("/account-settings/", self.ta_form_data, follow=True)
        self.assertEqual(str(response.context['status']), "Invalid first name.")

    def test_invalid_last_name(self):
        self.ta_form_data["last_name"] = "1234"
        response = self.client.post("/account-settings/", self.ta_form_data, follow=True)
        self.assertEqual(str(response.context['status']), "Invalid last name.")

    def test_invalid_email(self):
        self.ta_form_data["email"] = "fake.email"
        response = self.client.post("/account-settings/", self.ta_form_data, follow=True)
        self.assertEqual(str(response.context['status']), "Invalid email.")

    def test_invalid_phone_number(self):
        self.ta_form_data["phone_number"] = "not-a-phone-number"
        response = self.client.post("/account-settings/", self.ta_form_data, follow=True)
        self.assertEqual(str(response.context['status']), "Invalid phone number.")

    def test_invalid_address(self):
        self.ta_form_data["address"] = ""
        response = self.client.post("/account-settings/", self.ta_form_data, follow=True)
        self.assertEqual(str(response.context['status']), "Invalid address.")

    def test_invalid_date_of_birth(self):
        self.ta_form_data["birth_date"] = "October"
        response = self.client.post("/account-settings/", self.ta_form_data, follow=True)
        self.assertEqual(str(response.context['status']), "Invalid isoformat string: 'October'")


class UpdateSuccess(TestCase):
    def setUp(self):
        self.client = Client()

        self.ta = User(ROLE='TA',
                       FIRST_NAME='Jane',
                       LAST_NAME='Doe',
                       EMAIL='test@example.com',
                       PASSWORD_HASH='test_password',
                       PHONE_NUMBER='555-123-4567',
                       ADDRESS='1234 Elm St',
                       BIRTH_DATE=datetime.date(1995, 8, 30))

        self.ta.save()

        self.ta_form_data = {
            "first_name": self.ta.FIRST_NAME,
            "last_name": self.ta.LAST_NAME,
            "email": self.ta.EMAIL,
            "phone_number": self.ta.PHONE_NUMBER,
            "address": self.ta.ADDRESS,
            "birth_date": self.ta.BIRTH_DATE.isoformat(),
            "skills": ""
        }

        login_user(self.client, self.ta)

    def test_valid_submission(self):
        response = self.client.post("/account-settings/", self.ta_form_data, follow=True)
        self.assertEqual(str(response.context['status']), f'Your profile changes have been saved.')

    def test_valid_submission_updates_form(self):
        new_ta_form_data = {
            "first_name": "Jim",
            "last_name": "Geller",
            "email": "jimgeller@example.com",
            "phone_number": "123-456-7890",
            "address": "123 Main St, Anytown USA",
            "birth_date": "2000-01-01",
            "skills": "Python, SQL, Data Analysis"
        }

        response = self.client.post("/account-settings/", new_ta_form_data, follow=True)

        soup = BeautifulSoup(response.content, 'html.parser')

        for key, value in new_ta_form_data.items():
            if key is not "skills":
                self.assertIsNotNone(soup.find('input', {'value': value}), f"{key} {value} not found")
