import datetime

from django.test import TestCase, Client
from TA_Scheduling_App.models import User


class UserLoginSuccessTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User(ROLE='TA',
                         FIRST_NAME='Jane',
                         LAST_NAME='Doe',
                         EMAIL='test@example.com',
                         PASSWORD_HASH='test_password',
                         PHONE_NUMBER='555-123-4567',
                         ADDRESS='1234 Elm St',
                         BIRTH_DATE=datetime.date(1995, 8, 30))
        self.user.save()

    def test_user_credentials_valid(self):
        credentials = {
            "email": "test@example.com",
            "password": "test_password"
        }

        try:
            user = User.objects.get(EMAIL=credentials["email"])
            is_authenticated = user.PASSWORD_HASH == credentials["password"]
        except User.DoesNotExist:
            user = None
            is_authenticated = False

        self.assertTrue(is_authenticated)

    def test_user_login(self):
        credentials = {
            "email": "test@example.com",
            "password": "test_password"
        }

        response = self.client.post("/", credentials, follow=True)

        # Check if the user is logged in successfully using the session created by the post request
        is_authenticated = self.client.session.get('is_authenticated')

        self.assertTrue(is_authenticated)

    def test_user_redirected_to_dashboard(self):
        credentials = {
            "email": "test@example.com",
            "password": "test_password"
        }

        response = self.client.post("/", credentials, follow=True)

        self.assertRedirects(response, '/dashboard/')

    def test_user_information_in_session(self):
        credentials = {
            "email": "test@example.com",
            "password": "test_password"
        }

        response = self.client.post("/", credentials, follow=True)

        user_id_in_session = self.client.session.get('user_id')
        user_role_in_session = self.client.session.get('user_role')

        self.assertEqual(user_id_in_session, self.user.USER_ID)
        self.assertEqual(user_role_in_session, self.user.ROLE)

    def test_user_no_access_to_login_page_if_logged_in(self):
        credentials = {
            "email": "test@example.com",
            "password": "test_password"
        }

        # Log the user in first
        response = self.client.post("/", credentials, follow=True)

        # Try to access the login page again
        response = self.client.get("/")

        # Assert that the user is redirected to the dadhboard page
        self.assertRedirects(response, "/dashboard/")

    def test_user_can_logout(self):
        credentials = {
            "email": "test@example.com",
            "password": "test_password"
        }

        # Log the user in first
        response = self.client.post("/", credentials, follow=True)

        # Logout the user
        response = self.client.get("/?action=logout", follow=True)

        # Assert that the user is redirected to the login page and the session is cleared
        self.assertRedirects(response, "/")
        self.assertIsNone(self.client.session.get("is_authenticated"))
        self.assertIsNone(self.client.session.get("user_id"))
        self.assertIsNone(self.client.session.get("user_role"))


class UserLoginFailTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User(ROLE='TA',
                         FIRST_NAME='Jane',
                         LAST_NAME='Doe',
                         EMAIL='test@example.com',
                         PASSWORD_HASH='test_password',
                         PHONE_NUMBER='555-123-4567',
                         ADDRESS='1234 Elm St',
                         BIRTH_DATE=datetime.date(1995, 8, 30))
        self.user.save()

    def test_invalid_email(self):
        credentials = {
            "email": "invalid@example.com",
            "password": "test_password"
        }

        response = self.client.post("/", credentials)

        is_authenticated = self.client.session.get('is_authenticated')
        self.assertFalse(is_authenticated)
        self.assertEqual(response.context['status'], "Invalid email or password.")

    def test_invalid_password(self):
        credentials = {
            "email": "test@example.com",
            "password": "invalid_password"
        }

        response = self.client.post("/", credentials)

        is_authenticated = self.client.session.get('is_authenticated')
        self.assertFalse(is_authenticated)
        self.assertEqual(response.context['status'], "Invalid email or password.")

    def test_both_email_and_password_invalid(self):
        credentials = {
            "email": "invalid@example.com",
            "password": "invalid_password"
        }

        response = self.client.post("/", credentials)

        is_authenticated = self.client.session.get('is_authenticated')
        self.assertFalse(is_authenticated)
        self.assertEqual(response.context['status'], "Invalid email or password.")

    def test_empty_email_and_password(self):
        credentials = {
            "email": "",
            "password": ""
        }

        response = self.client.post("/", credentials)

        is_authenticated = self.client.session.get('is_authenticated')
        self.assertFalse(is_authenticated)
        self.assertEqual(response.context['status'], "Invalid email or password.")

    def test_empty_email(self):
        credentials = {
            "email": "",
            "password": "test_password"
        }

        response = self.client.post("/", credentials)

        is_authenticated = self.client.session.get('is_authenticated')
        self.assertFalse(is_authenticated)
        self.assertEqual(response.context['status'], "Invalid email or password.")

    def test_empty_password(self):
        credentials = {
            "email": "test@example.com",
            "password": ""
        }

        response = self.client.post("/", credentials)

        is_authenticated = self.client.session.get('is_authenticated')
        self.assertFalse(is_authenticated)
        self.assertEqual(response.context['status'], "Invalid email or password.")
