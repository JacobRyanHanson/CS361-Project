from datetime import date, time

from bs4 import BeautifulSoup
from django.test import TestCase, Client
from TA_Scheduling_App.models import Course, Section, User, CourseAssignment, SectionAssignment


def contains_text(tag, text):
    return tag.string is not None and text.strip() in tag.string.strip()


class TAViewSuccess(TestCase):

    def setUp(self):

        self.client = Client()

        self.TA = User(
            ROLE='TA',
            FIRST_NAME='John',
            LAST_NAME='Doe',
            EMAIL='TA@example.com',
            PASSWORD_HASH='ta_password',
            PHONE_NUMBER='555-123-4567',
            ADDRESS='123 Main St',
            BIRTH_DATE=date(1990, 1, 1),
            SKILLS="Research, Coding"
        )

        self.TA.save()

        course1 = Course.objects.create(
            COURSE_NUMBER=151,
            COURSE_NAME='Introduction to Computer Science',
            COURSE_DESCRIPTION='An introductory course to the world of computer science.',
            SEMESTER='Fall 2023',
            PREREQUISITES='',
            DEPARTMENT='Computer Science'
        )

        course2 = Course.objects.create(
            COURSE_NUMBER=122,
            COURSE_NAME='Data Structures',
            COURSE_DESCRIPTION='A course on fundamental data structures in computer science.',
            SEMESTER='Spring 2023',
            PREREQUISITES='Introduction to Computer Science',
            DEPARTMENT='Computer Science'
        )

        self.courses = [course1, course2]

        course_assignment_2 = CourseAssignment.objects.create(
            COURSE=course1,
            USER=self.TA,
            IS_GRADER=True
        )

        course_assignment_2.save()

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

        section_assignment1 = SectionAssignment.objects.create(
            COURSE_ASSIGNMENT=course_assignment_2,
            SECTION=section1
        )

        section_assignment2 = SectionAssignment.objects.create(
            COURSE_ASSIGNMENT=course_assignment_2,
            SECTION=section2
        )

        section_assignment1.save()
        section_assignment2.save()

        self.credentials = {
            "email": "TA@example.com",
            "password": "ta_password"
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

    def test_all_sections_are_visible(self):
        for section in self.expected_sections:
            for key, value in section.items():
                self.assertIsNotNone(self.soup.find(lambda tag: contains_text(tag, value)), f"{key} {value} not found")

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

    def test_course_name_shown(self):
        self.assertIsNotNone(self.soup.find(text=lambda t: "Computer Science 151 - Introduction to Computer Science"
                                                           in t.text), "info not found")



class TAViewFail(TestCase):

    def setUp(self):
        self.client = Client()

        self.TA = User(
            ROLE='TA',
            FIRST_NAME='John',
            LAST_NAME='Doe',
            EMAIL='TA@example.com',
            PASSWORD_HASH='ta_password',
            PHONE_NUMBER='555-123-4567',
            ADDRESS='123 Main St',
            BIRTH_DATE=date(1990, 1, 1),
            SKILLS="Research, Coding"
        )

        self.TA.save()

        self.credentials = {
            "email": "TA@example.com",
            "password": "ta_password"
        }

        self.course = Course.objects.create(
            COURSE_NUMBER=999,
            COURSE_NAME='Test Course',
            COURSE_DESCRIPTION='A test course.',
            SEMESTER='Fall 2023',
            PREREQUISITES='',
            DEPARTMENT='Computer Science'
        )

        self.course.save()

        course_assignment = CourseAssignment.objects.create(
            COURSE=self.course,
            USER=self.TA,
            IS_GRADER=True
        )

        course_assignment.save()

        self.section = Section.objects.create(
            SECTION_NUMBER=894,
            COURSE=self.course,
            BUILDING='Tech Building',
            ROOM_NUMBER='999',
            SECTION_START=time(9, 30),
            SECTION_END=time(10, 20)
        )

        section_assignment1 = SectionAssignment.objects.create(
            COURSE_ASSIGNMENT=course_assignment,
            SECTION=self.section
        )

        section_assignment1.save()

        self.section.save()

        self.client.post("/", self.credentials, follow=True)

        self.response = self.client.get("/ta-assignments/", follow=True)
        self.soup = BeautifulSoup(self.response.content, 'html.parser')

    def test_no_courses_in_system_and_none_visible(self):
        courses = Course.objects.all()

        if len(courses) == 0:
            self.assertIsNone(self.soup.find(lambda tag: tag.name == "h5" and contains_text(tag, "Course")),
                              "A course was found")

    def test_no_sections_in_system_and_none_visible(self):
        sections = Section.objects.all()

        if len(sections) == 0:
            self.assertIsNone(self.soup.find(lambda tag: tag.name == "h5" and contains_text(tag, "Section")),
                              "A section was found")

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

    def test_no_extra_course_info_displayed(self):
        self.assertIsNone(self.soup.find("Computer Science"), "Department is being displayed at the wrong time")
        self.assertIsNone(self.soup.find("A test course."),
                          "Course Description is being displayed at the wrong time")
