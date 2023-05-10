from datetime import date
from django.test import TestCase, Client
from TA_Scheduling_App.models import User


def login_as_admin(client: Client):
    admin = User(ROLE='ADMIN',
                 FIRST_NAME='John',
                 LAST_NAME='Doe',
                 EMAIL='admin@example.com',
                 PASSWORD_HASH='ad_password',
                 PHONE_NUMBER='555-123-4567',
                 ADDRESS='123 Main St',
                 BIRTH_DATE=date(1990, 1, 1))

    admin.save()

    client.post("/", {
        "email": admin.EMAIL,
        "password": admin.PASSWORD_HASH
    })


class CreationSuccess(TestCase):

    def setUp(self):
        self.client = Client()
        login_as_admin(self.client)

        self.ta_form_data = {
            'role': "TA",
            'first_name': "Joe",
            'last_name': "Smoe",
            'email': "joeSmoe@gmail.com",
            'phone_number': "999-999-9999",
            'address': "101 Drive",
            'birth_date': date(1990, 1, 1)
        }

        self.instructor_form_data = {
            'role': "INSTRUCTOR",
            'first_name': "John",
            'last_name': "Salem",
            'email': "johnsalem@gmail.com",
            'phone_number': "999-999-9999",
            'address': "101 Drive",
            'birth_date': date(1990, 1, 1)
        }

    def test_add_new_ta(self):
        response = self.client.post('/user-creation/', self.ta_form_data, follow=True)
        self.assertEqual(response.context['status'], 'Successfully created the user.')

    def test_add_new_instructor(self):
        response = self.client.post('/user-creation/', self.instructor_form_data, follow=True)
        self.assertEqual(response.context['status'], 'Successfully created the user.')


class CreationFail(TestCase):
    def setUp(self):
        self.client = Client()
        login_as_admin(self.client)

        self.ta_form_data = {
            'role': "TA",
            'first_name': "Joe",
            'last_name': "Smoe",
            'email': "joeSmoe@gmail.com",
            'phone_number': "999-999-9999",
            'address': "101 Drive",
            'birth_date': date(1990, 1, 1)
        }

        self.instructor_form_data = {
            'role': "INSTRUCTOR",
            'first_name': "John",
            'last_name': "Salem",
            'email': "joeSmoe@gmail.com",
            'phone_number': "999-999-9999",
            'address': "101 Drive",
            'birth_date': date(1990, 1, 1)
        }

    def test_invalid_email(self):
        response = self.client.post('/user-creation/', self.ta_form_data, follow=True)
        response = self.client.post('/user-creation/', self.instructor_form_data, follow=True)
        self.assertEqual(response.context['status'], 'Users with duplicate emails are not allowed.')

    def test_invalid_role(self):
        self.ta_form_data['role'] = ''
        response = self.client.post('/user-creation/', self.ta_form_data, follow=True)
        self.assertEqual(str(response.context['status']), 'Invalid role.')
