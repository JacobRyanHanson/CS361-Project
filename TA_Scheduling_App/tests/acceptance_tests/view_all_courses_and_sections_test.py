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

        self.instructor = User.objects.create(
            ROLE='INSTRUCTOR',
            FIRST_NAME='Alice',
            LAST_NAME='Smith',
            EMAIL='instructor@example.com',
            PHONE_NUMBER='555-987-6543',
            ADDRESS='456 Elm St',
            BIRTH_DATE=date(1995, 6, 15)
        )

        course1 = Course.objects.create(
            COURSE_NUMBER=151,
            INSTRUCTOR=self.instructor,
            COURSE_NAME='Introduction to Computer Science',
            COURSE_DESCRIPTION='An introductory course to the world of computer science.',
            SEMESTER='Fall 2023',
            PREREQUISITES='',
            DEPARTMENT='Computer Science'
        )

        course2 = Course.objects.create(
            COURSE_NUMBER=122,
            INSTRUCTOR=self.instructor,
            COURSE_NAME='Data Structures',
            COURSE_DESCRIPTION='A course on fundamental data structures in computer science.',
            SEMESTER='Spring 2023',
            PREREQUISITES='Introduction to Computer Science',
            DEPARTMENT='Computer Science'
        )

        self.courses = [course1, course2]

        section1 = Section.objects.create(
            SECTION_NUMBER=1,
            COURSE=course1,
            BUILDING='Tech Building',
            ROOM_NUMBER='111',
            SECTION_START=time(9, 30),
            SECTION_END=time(10, 20)
        )

        section2 = Section.objects.create(
            SECTION_NUMBER=2,
            COURSE=course1,
            BUILDING='Tech Building',
            ROOM_NUMBER='139',
            SECTION_START=time(9, 30),
            SECTION_END=time(11, 30)
        )

        self.sections = [section1, section2]

        self.credentials = {
            "email": "admin@example.com",
            "password": "ad_password"
        }

        self.client.post("/", self.credentials, follow=True)

        self.response = self.client.get("/ta-assignments/", follow=True)
        self.soup = BeautifulSoup(self.response.content, 'html.parser')

        self.expected_courses = [
            {
                'COURSE_NUMBER': '151',
                'COURSE_NAME': 'Introduction to Computer Science',
                'COURSE_DESCRIPTION': 'An introductory course to the world of computer science.',
                'SEMESTER': 'Fall 2023',
                'PREREQUISITES': '',
                'DEPARTMENT': 'Computer Science'
            },
            {
                'COURSE_NUMBER': '122',
                'COURSE_NAME': 'Data Structures',
                'COURSE_DESCRIPTION': 'A course on fundamental data structures in computer science.',
                'SEMESTER': 'Spring 2023',
                'PREREQUISITES': 'Introduction to Computer Science',
                'DEPARTMENT': 'Computer Science'
            }
        ]

        self.expected_sections = [
            {
                'SECTION_NUMBER': '1',
                'COURSE_NUMBER': '151',
                'BUILDING': 'Tech Building',
                'ROOM_NUMBER': '111',
                'SECTION_START': '9:30',
                'SECTION_END': '10:20'
            },
            {
                'SECTION_NUMBER': '2',
                'COURSE_NUMBER': '151',
                'BUILDING': 'Tech Building',
                'ROOM_NUMBER': '139',
                'SECTION_START': '9:30',
                'SECTION_END': '11:30'
            }
        ]

    def test_all_courses_are_visible(self):
        for course in self.expected_courses:
            for key, value in course.items():
                self.assertIsNotNone(self.soup.find(lambda tag: contains_text(tag, value)), f"{key} {value} not found")

    def test_all_sections_are_visible(self):
        for section in self.expected_sections:
            for key, value in section.items():
                self.assertIsNotNone(self.soup.find(lambda tag: contains_text(tag, value)), f"{key} {value} not found")

    def test_all_instructors_are_visible(self):
        expected_instructors = [
            {
                'FIRST_NAME': 'Alice',
                'LAST_NAME': 'Smith',
            }
        ]

        for instructor in expected_instructors:
            for key, value in instructor.items():
                self.assertIsNotNone(self.soup.find(lambda tag: contains_text(tag, value)), f"{key} {value} not found")

        # Find value of input field (not directly in HTML)
        self.assertIsNotNone(self.soup.find('input', {'type': 'email', 'value': 'instructor@example.com'}), f"Email not found")

    def test_no_extra_courses_exist(self):
        # Check for any unexpected courses
        for course in Course.objects.all():
            course_data = {
                'COURSE_NUMBER': str(course.COURSE_NUMBER),
                'COURSE_NAME': course.COURSE_NAME,
                'COURSE_DESCRIPTION': course.COURSE_DESCRIPTION,
                'SEMESTER': course.SEMESTER,
                'PREREQUISITES': course.PREREQUISITES,
                'DEPARTMENT': course.DEPARTMENT
            }
            self.assertIn(course_data, self.expected_courses, f"Unexpected course found: {course_data}")

    def test_no_extra_sections_exist(self):
        # Check for any unexpected sections
        for section in Section.objects.all():
            section_data = {
                'SECTION_NUMBER': str(section.SECTION_NUMBER),
                'COURSE_NUMBER': str(section.COURSE.COURSE_NUMBER),
                'BUILDING': section.BUILDING,
                'ROOM_NUMBER': section.ROOM_NUMBER,
                'SECTION_START': section.SECTION_START.strftime('%H:%M').lstrip('0'),
                'SECTION_END': section.SECTION_END.strftime('%H:%M').lstrip('0')
            }
            self.assertIn(section_data, self.expected_sections, f"Unexpected section found: {section_data}")

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

        self.credentials = {
            "email": "admin@example.com",
            "password": "ad_password"
        }

        self.course = Course.objects.create(
            COURSE_NUMBER=999,
            INSTRUCTOR=None,
            COURSE_NAME='Test Course',
            COURSE_DESCRIPTION='A test course.',
            SEMESTER='Fall 2023',
            PREREQUISITES='',
            DEPARTMENT='Computer Science'
        )

        self.course.save()

        self.section = Section.objects.create(
            SECTION_NUMBER=894,
            COURSE=self.course,
            BUILDING='Tech Building',
            ROOM_NUMBER='999',
            SECTION_START=time(9, 30),
            SECTION_END=time(10, 20)
        )

        self.section.save()

        self.client.post("/", self.credentials, follow=True)

        self.response = self.client.get("/ta-assignments/", follow=True)
        self.soup = BeautifulSoup(self.response.content, 'html.parser')

    def test_no_courses_in_system_and_none_visible(self):
        courses = Course.objects.all()

        if len(courses) == 0:
            self.assertIsNone(self.soup.find(lambda tag: tag.name == "h5" and contains_text(tag, "Course")), "A course was found")

    def test_no_sections_in_system_and_none_visible(self):
        sections = Section.objects.all()

        if len(sections) == 0:
            self.assertIsNone(self.soup.find(lambda tag: tag.name == "h5" and contains_text(tag, "Section")), "A section was found")

    def test_course_not_visible_when_deleted(self):
        self.course.delete()
        self.response = self.client.get("/ta-assignments/", follow=True)
        self.soup = BeautifulSoup(self.response.content, 'html.parser')
        self.assertIsNone(self.soup.find(lambda tag: contains_text(tag, 'Test Course')), "Deleted course was found")

    def test_section_not_visible_when_deleted(self):
        self.section.delete()
        self.response = self.client.get("/ta-assignments/", follow=True)
        self.soup = BeautifulSoup(self.response.content, 'html.parser')
        self.assertIsNone(self.soup.find(lambda tag: contains_text(tag, '894')), "Deleted section was found")




