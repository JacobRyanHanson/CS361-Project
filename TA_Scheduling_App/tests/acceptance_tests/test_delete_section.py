import datetime
from datetime import date, time
from bs4 import BeautifulSoup
from django.test import TestCase, Client
from TA_Scheduling_App.models import User, Course, Section, CourseAssignment, SectionAssignment


def contains_text(tag, text):
    return tag.string is not None and text.strip() in tag.string.strip()


class DeleteSectionSuccessTest(TestCase):
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
            BIRTH_DATE=datetime.date(1990, 1, 1)
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

        self.course = Course(
            COURSE_NUMBER=151,
            COURSE_NAME='Introduction to Computer Science',
            COURSE_DESCRIPTION='An introductory course to the world of computer science.',
            SEMESTER='Fall 2023',
            PREREQUISITES='',
            DEPARTMENT='Computer Science'
        )

        self.course.save()

        self.section = Section(
            SECTION_TYPE="LAB",
            SECTION_NUMBER=1,
            COURSE=self.course,
            BUILDING='Tech Building',
            ROOM_NUMBER='105',
            SECTION_START=time(9, 30),
            SECTION_END=time(10, 20)
        )

        self.section.save()

        self.newSection = Section(
            SECTION_TYPE="LAB",
            SECTION_NUMBER=7,
            COURSE=self.course,
            BUILDING='Tech',
            ROOM_NUMBER='555',
            SECTION_START=time(9, 30),
            SECTION_END=time(10, 20)
        )

        self.newSection.save()

        self.thirdSection = Section(
            SECTION_TYPE="LAB",
            SECTION_NUMBER=11,
            COURSE=self.course,
            BUILDING='Tech',
            ROOM_NUMBER='555',
            SECTION_START=time(9, 30),
            SECTION_END=time(10, 20)
        )

        self.thirdSection.save()

        # Log the user in
        self.credentials = {
            "email": "admin@example.com",
            "password": "ad_password"
        }
        self.client.post("/", self.credentials, follow=True)

    def test_delete_section_from_system(self):
        self.assertEqual(len(Section.objects.filter(SECTION_NUMBER=self.section.SECTION_NUMBER)), 1)

        self.client.post("/ta-assignments/", {"section_id": self.section.SECTION_ID})

        self.assertEqual(len(Section.objects.filter(SECTION_NUMBER=self.section.SECTION_NUMBER)), 0)

    def test_delete_section_removed_from_page(self):
        self.assertEqual(len(Section.objects.filter(SECTION_NUMBER=self.thirdSection.SECTION_NUMBER)), 1)

        response = self.client.post("/ta-assignments/", {"section_id": self.thirdSection.SECTION_ID})

        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertIsNone(soup.find(lambda tag: contains_text(tag, str(self.thirdSection.SECTION_NUMBER))),
                          f"Deleted section with number 11 was found")

    def test_delete_section_displays_success_message(self):
        self.assertEqual(len(Section.objects.filter(SECTION_NUMBER=self.newSection.SECTION_NUMBER)), 1)

        response = self.client.post("/ta-assignments/", {"section_id": self.newSection.SECTION_ID}, follow=True)
        self.assertEqual(str(response.context['status']), 'Section has been deleted.')


class DeleteSectionRemoveRestTest(TestCase):
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
            BIRTH_DATE=datetime.date(1990, 1, 1)
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
            LAST_NAME='Smith',
            EMAIL='ta@example.com',
            PASSWORD_HASH='add_password',
            PHONE_NUMBER='555-123-4567',
            ADDRESS='123 Main St',
            BIRTH_DATE=date(1990, 1, 1)
        )

        self.ta.save()

        self.course = Course(
            COURSE_NUMBER=151,
            COURSE_NAME='Introduction to Computer Science',
            COURSE_DESCRIPTION='An introductory course to the world of computer science.',
            SEMESTER='Fall 2023',
            PREREQUISITES='',
            DEPARTMENT='Computer Science'
        )

        self.course.save()

        self.section = Section(
            SECTION_TYPE="LAB",
            SECTION_NUMBER=1,
            COURSE=self.course,
            BUILDING='Tech Building',
            ROOM_NUMBER='999',
            SECTION_START=time(9, 30),
            SECTION_END=time(10, 20)
        )

        self.section.save()

        self.newSection = Section(
            SECTION_TYPE="LAB",
            SECTION_NUMBER=7,
            COURSE=self.course,
            BUILDING='Tech Building',
            ROOM_NUMBER='555',
            SECTION_START=time(9, 30),
            SECTION_END=time(10, 20)
        )

        self.newSection.save()

        self.courseAssignment = CourseAssignment(
            COURSE=self.course,
            USER=self.ta,
            IS_GRADER=True
        )

        self.courseAssignment.save()

        self.sectionAssignment = SectionAssignment(
            COURSE_ASSIGNMENT=self.courseAssignment,
            SECTION=self.section
        )

        self.sectionAssignment.save()

        # Log the user in
        self.credentials = {
            "email": "admin@example.com",
            "password": "ad_password"
        }
        self.client.post("/", self.credentials, follow=True)

    def test_delete_section_and_assignments(self):
        self.assertEqual(len(Section.objects.filter(SECTION_NUMBER=self.section.SECTION_NUMBER)), 1)
        self.client.post("/ta-assignments/", {"section_id": self.section.SECTION_ID}, follow=True)

        self.assertEqual(len(Section.objects.filter(SECTION_NUMBER=self.section.SECTION_NUMBER)), 0)
        self.assertFalse(SectionAssignment.objects.filter(SECTION=self.section).exists())

    def test_delete_section_assignments_removed_from_page(self):
        self.assertEqual(len(Section.objects.filter(SECTION_NUMBER=self.newSection.SECTION_NUMBER)), 1)

        sectionNewAssignment = SectionAssignment(
            COURSE_ASSIGNMENT=self.courseAssignment,
            SECTION=self.newSection
        )
        sectionNewAssignment.save()

        response = self.client.post("/ta-assignments/", {"section_id": self.newSection.SECTION_ID}, follow=True)

        soup = BeautifulSoup(response.content, 'html.parser')
        # Check if the assignments has been removed from the page
        self.assertIsNone(soup.find(lambda tag: contains_text(tag, str(sectionNewAssignment))),
                          f"TA Assignment for deleted section 7 with TA Jane was found")

