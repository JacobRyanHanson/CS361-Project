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

class ViewSkills(TestCase):
    def setUp(self):
        self.client = Client()

        self.ta = User(ROLE='TA',
                       FIRST_NAME='Jane',
                       LAST_NAME='Doe',
                       EMAIL='test@example.com',
                       PASSWORD_HASH='test_password',
                       PHONE_NUMBER='555-123-4567',
                       ADDRESS='1234 Elm St',
                       BIRTH_DATE=datetime.date(1995, 8, 30),
                       SKILLS="Management, Communication")
        self.ta.save()

        login_user(self.client, self.ta)

        self.response = self.client.get("/account-settings/", follow=True)
        self.soup = BeautifulSoup(self.response.content, 'html.parser')

    def test_skills_field_renders(self):
        # Test if the skills field is actually displayed on the html rendered
        self.assertIsNotNone(self.soup.find(lambda tag: contains_text(tag, "Skills:")), "Skills field not rendered")

    def test_skills_form_prefilled(self):
        skills = self.soup.find('textarea', {'name': 'skills'})
        self.assertEqual(skills.text, self.ta.SKILLS)

class SkillsAbsentNonTA(TestCase):
    def setUp(self):
        self.client = Client()

    def test_admin_settings_no_skills(self):
        # login as admin and test that the skills field is not visible
        admin = User(ROLE='ADMIN',
                     FIRST_NAME='John',
                     LAST_NAME='Doe',
                     EMAIL='admin@example.com',
                     PASSWORD_HASH='ad_password',
                     PHONE_NUMBER='555-123-4567',
                     ADDRESS='123 Main St',
                     BIRTH_DATE=datetime.date(1990, 1, 1),
                     SKILLS="Management, Communication")

        login_user(self.client, admin)
        response = self.client.get("/account-settings/", follow=True)
        soup = BeautifulSoup(response.content, 'html.parser')
        skills = soup.find('textarea', {'name': 'skills'})
        self.assertIsNone(skills, 'Skills not omitted from page for ADMIN')

    def test_instructor_settings_no_skills(self):
        # login as instructor and test that the skills field is not visible
        instructor = User(ROLE='INSTRUCTOR',
                     FIRST_NAME='Alice',
                     LAST_NAME='Smith',
                     EMAIL='instructor_2@example.com',
                     PHONE_NUMBER='555-987-6543',
                     ADDRESS='456 Elm St',
                     BIRTH_DATE=datetime.date(1995, 6, 15),
                     SKILLS="Management, Communication")

        login_user(self.client, instructor)
        response = self.client.get("/account-settings/", follow=True)
        soup = BeautifulSoup(response.content, 'html.parser')
        skills = soup.find('textarea', {'name': 'skills'})
        self.assertIsNone(skills, 'Skills not omitted from page for INSTRUCTOR')

class UpdateSkillsSuccess(TestCase):
    def setUp(self):
        self.client = Client()

        self.ta = User(ROLE='TA',
                       FIRST_NAME='Jane',
                       LAST_NAME='Doe',
                       EMAIL='test@example.com',
                       PASSWORD_HASH='test_password',
                       PHONE_NUMBER='555-123-4567',
                       ADDRESS='1234 Elm St',
                       BIRTH_DATE=datetime.date(1995, 8, 30),
                       SKILLS="Management, Communication")
        self.ta.save()

        self.ta_form_data = {
            "first_name": self.ta.FIRST_NAME,
            "last_name": self.ta.LAST_NAME,
            "email": self.ta.EMAIL,
            "phone_number": self.ta.PHONE_NUMBER,
            "address": self.ta.ADDRESS,
            "birth_date": self.ta.BIRTH_DATE.isoformat(),
            "skills": self.ta.SKILLS
        }

        login_user(self.client, self.ta)

    def test_update_skills_success_message(self):
        self.ta_form_data['skills'] = "Management"
        response = self.client.post("/account-settings/", self.ta_form_data, follow=True)
        self.assertEqual(response.context['status'], 'Your profile changes have been saved.', 'Success message not returned')

    def test_skills_removed(self):
        self.ta_form_data['skills'] = ""
        response = self.client.post("/account-settings/", self.ta_form_data, follow=True)
        soup = BeautifulSoup(response.content, 'html.parser')
        skills = soup.find('textarea', {'name': 'skills'})
        self.assertEqual(skills.text, '', 'Skills not field not emptied')

class UpdateSkillsFail(TestCase):
    def setUp(self):
        self.client = Client()

        self.ta = User(ROLE='TA',
                       FIRST_NAME='Jane',
                       LAST_NAME='Doe',
                       EMAIL='test@example.com',
                       PASSWORD_HASH='test_password',
                       PHONE_NUMBER='555-123-4567',
                       ADDRESS='1234 Elm St',
                       BIRTH_DATE=datetime.date(1995, 8, 30),
                       SKILLS="Management, Communication")
        self.ta.save()

        self.ta_form_data = {
            "first_name": self.ta.FIRST_NAME,
            "last_name": self.ta.LAST_NAME,
            "email": self.ta.EMAIL,
            "phone_number": self.ta.PHONE_NUMBER,
            "address": self.ta.ADDRESS,
            "birth_date": self.ta.BIRTH_DATE.isoformat(),
            "skills": self.ta.SKILLS
        }

        login_user(self.client, self.ta)

    def test_skills_too_long(self):
        long_skills = ""
        for _ in range(500):
            long_skills += 'a'
        self.ta_form_data['skills'] = long_skills
        response = self.client.post("/account-settings/", self.ta_form_data, follow=True)
        self.assertEqual(str(response.context['status']), 'Invalid list of skills.', 'Long skills field not rejected')

    def test_skills_omitted(self):
        del self.ta_form_data['skills']

        with self.assertRaises(KeyError, msg='Skills omitted without error'):
            self.client.post("/account-settings/", self.ta_form_data, follow=True)
