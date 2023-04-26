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
        self.monkey = Client()
        login_as_admin(self.monkey)

    def test_AddNewTA(self):
        response = self.monkey.post('/user-creation/', {'role': "TA",
                                                        'firstName': "Joe",
                                                        'lastName': "Smoe",
                                                        'email': "joeSmoe@gmail.com",
                                                        'phoneNumber': "999-999-9999",
                                                        'address': "101 Drive",
                                                        'birthDate': date(1990, 1, 1)})
        self.assertEqual(response.context['status'], 'Successfully created the user.')

    def test_AddNewInstr(self):
        response = self.monkey.post('/user-creation/', {'role': "INSTRUCTOR",
                                                        'firstName': "Jeff",
                                                        'lastName': "Smoe",
                                                        'email': "jeffSmoe@gmail.com",
                                                        'phoneNumber': "999-999-9998",
                                                        'address': "102 Drive",
                                                        'birthDate': date(1990, 1, 2)})
        self.assertEqual(response.context['status'], 'Successfully created the user.')


class CreationFail(TestCase):
    def setUp(self):
        self.monkey = Client()
        login_as_admin(self.monkey)

    def test_InvalidEmail(self):
        response = self.monkey.post('/user-creation/', {'role': "TA",
                                                        'firstName': "Joe",
                                                        'lastName': "Smoe",
                                                        'email': "admin@example.com",
                                                        'phoneNumber': "999-999-9999",
                                                        'address': "101 Drive",
                                                        'birthDate': date(1990, 1, 1)})
        self.assertEqual(response.context['status'], 'Users with duplicate emails are not allowed.')

    def test_InvalidRole(self):
        response = self.monkey.post('/user-creation/', {'role': "",
                                                        'firstName': "Joe",
                                                        'lastName': "Smoe",
                                                        'email': "admin@example.com",
                                                        'phoneNumber': "999-999-9999",
                                                        'address': "101 Drive",
                                                        'birthDate': date(1990, 1, 1)})
        self.assertEqual(str(response.context['status']), 'Invalid role')