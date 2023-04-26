import datetime
import django.urls

from bs4 import BeautifulSoup, ResultSet
from django.test import TestCase, Client
from TA_Scheduling_App.models import User

PAGE = django.urls.reverse("account_settings")


def create_example_ta():  # create example user used for all account settings test classes
    user = User(ROLE='TA',
                FIRST_NAME='Jane',
                LAST_NAME='Doe',
                EMAIL='test@example.com',
                PASSWORD_HASH='test_password',
                PHONE_NUMBER='555-123-4567',
                ADDRESS='1234 Elm St',
                BIRTH_DATE=datetime.date(1995, 8, 30))
    user.save()
    return user


def login_user(client: Client, user):
    credentials = {
        "email": user.EMAIL,
        "password": user.PASSWORD_HASH
    }
    client.post("/", credentials, follow=True)


def form_data_from_user(user: User) -> dict:
    return {
        "firstName": user.FIRST_NAME,
        "lastName": user.LAST_NAME,
        "email": user.EMAIL,
        "phoneNumber": user.PHONE_NUMBER,
        "address": user.ADDRESS,
        "dateOfBirth": user.BIRTH_DATE.isoformat()
    }


def get_form_fields(soup: BeautifulSoup) -> dict[str, str]:
    fields = soup.find_all("input")
    return {field["name"]: field["value"] for field in fields}


class LoadFailNoAuth(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = create_example_ta()

    def test_noauth_get_redirects(self):
        # if a user is not logged in, are they directed to log in before viewing this page?
        response = self.client.get(PAGE)
        self.assertRedirects(response, "/")

    def test_noauth_post_rejects(self):
        # if a user is not logged in, this is an illegal attempt to modify info!
        # content of request does not matter.
        response = self.client.post(PAGE, None)
        self.assertEqual(response.status_code, 403)


class LoadSuccess(TestCase):
    def setUp(self):
        # create example user and log in for testing rendering
        self.client = Client()
        self.user = create_example_ta()
        login_user(self.client, self.user)
        self.response = self.client.get(PAGE)
        self.soup = BeautifulSoup(self.response.content)
        self.data = form_data_from_user(self.user)

    def test_auth_success(self):
        # is the account settings page viewable for a logged in user?
        self.assertEqual(self.response.status_code, 200)

    def test_template_renders(self):
        self.assertTemplateUsed(self.response, "account-settings.html")

    def test_form_prefilled(self):
        # is the account settings form filled with existing user information?
        fields = get_form_fields(self.soup)
        for name, value in self.data.items():
            # fields of the user info which the form fields should be displaying
            # field value should equal real value
            self.assertEqual(fields[name], value)


class UpdateFail(TestCase):
    def post_user(self) -> str:
        # POST account-settings with the user object in 'data' and return the status message
        self.response = self.client.post(PAGE, self.data)
        return str(self.response.context["status"])

    def setUp(self):
        self.client = Client()
        self.user = create_example_ta()
        login_user(self.client, self.user)
        # create user post data dict which we can edit fields to be invalid
        self.data = form_data_from_user(self.user)

    def test_invalid_first_name(self):
        self.data["firstName"] = "1234"
        self.assertEqual(self.post_user(), "Invalid first name")

    def test_invalid_last_name(self):
        self.data["lastName"] = "1234"
        self.assertEqual(self.post_user(), "Invalid last name")

    def test_invalid_email(self):
        self.data["email"] = "fake.email"
        self.assertEqual(self.post_user(), "Invalid email")

    def test_invalid_phone_number(self):
        self.data["phoneNumber"] = "not-a-phone-number"
        self.assertEqual(self.post_user(), "Invalid phone number")

    def test_invalid_address(self):
        self.data["address"] = ""
        self.assertEqual(self.post_user(), "Invalid address")

    def test_invalid_date_of_birth(self):
        self.data["dateOfBirth"] = "October"
        self.assertEqual(self.post_user(), "Invalid birth date")


class UpdateSuccess(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = create_example_ta()
        login_user(self.client, self.user)
        data = form_data_from_user(self.user)

        # modify user data submitted to form to "valid" information for these success tests.
        data["firstName"] = "John"
        data["lastName"] = "Doe"
        data["email"] = "john.doe@example.com"
        data["phoneNumber"] = "555-123-4567"
        data["address"] = "123 Main St"
        data["dateOfBirth"] = datetime.date(1995, 8, 30).isoformat()

        self.data = data
        self.response = self.client.post(PAGE, data)

    def test_valid_submission_updates_database(self):
        self.user.refresh_from_db()
        self.assertEqual(self.user.FIRST_NAME, self.data["firstName"])
        self.assertEqual(self.user.LAST_NAME, self.data["lastName"])
        self.assertEqual(self.user.EMAIL, self.data["email"])
        self.assertEqual(self.user.PHONE_NUMBER, self.data["phoneNumber"])
        self.assertEqual(self.user.ADDRESS, self.data["address"])
        self.assertEqual(self.user.BIRTH_DATE.isoformat(), self.data["dateOfBirth"])

    def test_valid_submission_updates_status(self):
        self.assertEqual(self.response.context["status"], "Your profile changes have been successfully saved.")

    def test_valid_submission_updates_form(self):
        soup = BeautifulSoup(self.response.content)
        fields = get_form_fields(soup)
        for name, value in self.data.items():
            # field value should equal submitted data value
            self.assertEqual(fields[name], value)

