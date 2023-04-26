import datetime
from datetime import date, time
from bs4 import BeautifulSoup
from django.test import TestCase, Client
from TA_Scheduling_App.models import User, Course, Section

def contains_text(tag, text):
    return tag.string is not None and text.strip() in tag.string.strip()
class DeleteCourseSuccessTest(TestCase):
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
            INSTRUCTOR=self.instructor,
            COURSE_NAME='Introduction to Computer Science',
            COURSE_DESCRIPTION='An introductory course to the world of computer science.',
            SEMESTER='Fall 2023',
            PREREQUISITES='',
            DEPARTMENT='Computer Science'
        )

        self.course.save()

        self.newCourse = Course(
            COURSE_NUMBER=171,
            INSTRUCTOR=self.instructor,
            COURSE_NAME='Introduction to Software',
            COURSE_DESCRIPTION='An introductory course to the world of Software',
            SEMESTER='Fall 2023',
            PREREQUISITES='',
            DEPARTMENT='Computer Science'
        )

        self.newCourse.save()

        self.thirdCourse = Course(
            COURSE_NUMBER=191,
            INSTRUCTOR=self.instructor,
            COURSE_NAME='Introduction to Data',
            COURSE_DESCRIPTION='An introductory course to the world of data.',
            SEMESTER='Fall 2023',
            PREREQUISITES='',
            DEPARTMENT='Computer Science'
        )

        self.thirdCourse.save()

        # Log the user in
        self.credentials = {
            "email": "admin@example.com",
            "password": "ad_password"
        }
        self.client.post("/", self.credentials, follow=True)

    def test_delete_course_from_system(self):
        self.assertEqual(len(Course.objects.filter(COURSE_NUMBER=self.course.COURSE_NUMBER)), 1)

        self.client.post("/ta-assignments/", {"course_id": self.course.COURSE_ID}, follow=True)

        self.assertEqual(len(Course.objects.filter(COURSE_NUMBER=self.course.COURSE_NUMBER)), 0)

    def test_delete_course_removed_from_page(self):
        self.assertEqual(len(Course.objects.filter(COURSE_NUMBER=self.newCourse.COURSE_NUMBER)), 1)

        response = self.client.post("/ta-assignments/", {"course_id": self.newCourse.COURSE_ID}, follow=True)
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertIsNone(soup.find(lambda tag: contains_text(tag, str(self.newCourse.COURSE_NUMBER))),
                          f"Deleted section with number 171 was found")

    def test_delete_section_displays_success_message(self):
        self.assertEqual(len(Course.objects.filter(COURSE_NUMBER=self.thirdCourse.COURSE_NUMBER)), 1)

        response = self.client.post("/ta-assignments/", {"course_id": self.thirdCourse.COURSE_ID}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['status']), 'Course with ID 3 has been deleted.')


class DeleteCourseFailTest(TestCase):
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
            INSTRUCTOR=self.instructor,
            COURSE_NAME='Introduction to Computer Science',
            COURSE_DESCRIPTION='An introductory course to the world of computer science.',
            SEMESTER='Fall 2023',
            PREREQUISITES='',
            DEPARTMENT='Computer Science'
        )

        self.course.save()

        self.newCourse = Course(
            COURSE_NUMBER=300,
            INSTRUCTOR=self.instructor,
            COURSE_NAME='Intermediate Computer Programming',
            COURSE_DESCRIPTION='An intermediate course.',
            SEMESTER='Fall 2023',
            PREREQUISITES='',
            DEPARTMENT='Computer Science'
        )

        self.newCourse.save()

        self.section = Section(
            SECTION_NUMBER=1,
            COURSE=self.course,
            BUILDING='Tech Building',
            ROOM_NUMBER='999',
            SECTION_START=time(9, 30),
            SECTION_END=time(10, 20)
        )

        self.section.save()

        self.newSection = Section(
            SECTION_NUMBER=32,
            COURSE=self.newCourse,
            BUILDING='Tech Building',
            ROOM_NUMBER='999',
            SECTION_START=time(9, 30),
            SECTION_END=time(10, 20)
        )

        self.newSection.save()

        # Log the user in
        self.credentials = {
            "email": "admin@example.com",
            "password": "ad_password"
        }
        self.client.post("/", self.credentials, follow=True)

    def test_delete_course_and_section(self):
        self.assertEqual(len(Course.objects.filter(COURSE_NUMBER=self.course.COURSE_NUMBER)), 1)
        self.client.post("/ta-assignments/", {"course_id": self.course.COURSE_ID}, follow=True)

        self.assertEqual(len(Course.objects.filter(COURSE_NUMBER=self.course.COURSE_NUMBER)), 0)
        self.assertEqual(len(Section.objects.filter(SECTION_NUMBER=self.section.SECTION_NUMBER)), 0)

    def test_delete_course_sections_removed_from_page(self):
        self.assertEqual(len(Course.objects.filter(COURSE_NUMBER=self.course.COURSE_NUMBER)), 1)

        response = self.client.post("/ta-assignments/", {"course_id": self.newCourse.COURSE_ID}, follow=True)
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        # Check if the assignments has been removed from the page
        self.assertIsNone(soup.find(lambda tag: contains_text(tag, str(self.newSection))),
                          f"Section (32) assigned to deleted course (300) was found")
