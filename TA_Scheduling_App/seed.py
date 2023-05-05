import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TA_Scheduling_Project.settings')
django.setup()

from TA_Scheduling_App.models.User import User
from TA_Scheduling_App.models.Course import Course
from TA_Scheduling_App.models.Section import Section
from TA_Scheduling_App.models.Course_Assignment import CourseAssignment
from TA_Scheduling_App.models.Section_Assignment import SectionAssignment
from datetime import date, time
from django.core.management import call_command
from django.db import connection


def reset_app(app_name):
    # First, disable foreign key checks
    cursor = connection.cursor()
    cursor.execute('PRAGMA foreign_keys = OFF;')

    # Then, flush the database to drop all tables
    call_command('flush', interactive=False)

    # Finally, re-enable foreign key checks
    cursor.execute('PRAGMA foreign_keys = ON;')


def insert_data():
    # Insert users
    admin = User.objects.create(
        ROLE='ADMIN',
        FIRST_NAME='John',
        LAST_NAME='Doe',
        EMAIL='john.doe@example.com',
        PASSWORD_HASH='test1',
        PHONE_NUMBER='555-123-4567',
        ADDRESS='123 Main St',
        BIRTH_DATE=date(1990, 1, 1)
    )

    instructor_1 = User.objects.create(
        ROLE='INSTRUCTOR',
        FIRST_NAME='Alice',
        LAST_NAME='Smith',
        EMAIL='alice.smith@example.com',
        PASSWORD_HASH='test2',
        PHONE_NUMBER='555-987-6543',
        ADDRESS='456 Elm St',
        BIRTH_DATE=date(1985, 6, 15)
    )

    instructor_2 = User.objects.create(
        ROLE='INSTRUCTOR',
        FIRST_NAME='Michael',
        LAST_NAME='Brown',
        EMAIL='michael.brown@example.com',
        PASSWORD_HASH='test3',
        PHONE_NUMBER='555-987-6578',
        ADDRESS='321 Pine St',
        BIRTH_DATE=date(1988, 10, 20)
    )

    ta_1 = User.objects.create(
        ROLE='TA',
        FIRST_NAME='Emma',
        LAST_NAME='Johnson',
        EMAIL='emma.johnson@example.com',
        PASSWORD_HASH='test4',
        PHONE_NUMBER='555-123-4587',
        ADDRESS='789 Oak St',
        BIRTH_DATE=date(1992, 3, 12),
        SKILLS="Management, Communication"
    )

    ta_2 = User.objects.create(
        ROLE='TA',
        FIRST_NAME='Sophia',
        LAST_NAME='Williams',
        EMAIL='sophia.williams@example.com',
        PASSWORD_HASH='test5',
        PHONE_NUMBER='555-123-4599',
        ADDRESS='147 Maple St',
        BIRTH_DATE=date(1994, 7, 25),
        SKILLS="Research, Writing"
    )

    # Insert courses
    course_1 = Course.objects.create(
        COURSE_NUMBER=101,
        COURSE_NAME='Introduction to Computer Science',
        COURSE_DESCRIPTION='An introductory course to the world of computer science.',
        SEMESTER='Fall 2023',
        PREREQUISITES='',
        DEPARTMENT='Computer Science'
    )

    course_2 = Course.objects.create(
        COURSE_NUMBER=102,
        COURSE_NAME='Data Structures',
        COURSE_DESCRIPTION='A course on fundamental data structures in computer science.',
        SEMESTER='Spring 2023',
        PREREQUISITES='Introduction to Computer Science',
        DEPARTMENT='Computer Science'
    )

    course_3 = Course.objects.create(
        COURSE_NUMBER=103,
        COURSE_NAME='Algorithms',
        COURSE_DESCRIPTION='A course on fundamental algorithms in computer science.',
        SEMESTER='Fall 2023',
        PREREQUISITES='Data Structures',
        DEPARTMENT='Computer Science'
    )

    course_4 = Course.objects.create(
        COURSE_NUMBER=104,
        COURSE_NAME='Operating Systems',
        COURSE_DESCRIPTION='A course on the principles of operating systems.',
        SEMESTER='Spring 2023',
        PREREQUISITES='Data Structures',
        DEPARTMENT='Computer Science'
    )

    # Insert sections
    section_1 = Section.objects.create(
        SECTION_TYPE="LECTURE",
        SECTION_NUMBER=1,
        COURSE=course_1,
        BUILDING='Tech Building',
        ROOM_NUMBER='101',
        SECTION_START=time(9, 0),
        SECTION_END=time(10, 15)
    )

    section_2 = Section.objects.create(
        SECTION_TYPE="LAB",
        SECTION_NUMBER=2,
        COURSE=course_1,
        BUILDING='Tech Building',
        ROOM_NUMBER='102',
        SECTION_START=time(10, 30),
        SECTION_END=time(11, 45)
    )

    section_3 = Section.objects.create(
        SECTION_TYPE="LAB",
        SECTION_NUMBER=1,
        COURSE=course_3,
        BUILDING='Tech Building',
        ROOM_NUMBER='103',
        SECTION_START=time(12, 0),
        SECTION_END=time(13, 15)
    )

    section_4 = Section.objects.create(
        SECTION_TYPE="LECTURE",
        SECTION_NUMBER=2,
        COURSE=course_4,
        BUILDING='Tech Building',
        ROOM_NUMBER='104',
        SECTION_START=time(14, 0),
        SECTION_END=time(15, 15)
    )

    # Assign an instructor to course 1
    course_assignment_1 = CourseAssignment.objects.create(
        COURSE=course_1,
        USER=instructor_1,
    )

    # Assign a TA to course 1
    course_assignment_2 = CourseAssignment.objects.create(
        COURSE=course_1,
        USER=ta_1,
        IS_GRADER=True
    )

    # Assign an instructor to course 3
    course_assignment_3 = CourseAssignment.objects.create(
        COURSE=course_3,
        USER=instructor_2,
    )

    # Assign a TA to course 3
    course_assignment_4 = CourseAssignment.objects.create(
        COURSE=course_3,
        USER=ta_2,
        IS_GRADER=False
    )

    # Assign an instructor to course 1, section 1
    section_assignment_1 = SectionAssignment.objects.create(
        COURSE_ASSIGNMENT=course_assignment_1,
        SECTION=section_1
    )

    # Assign a TA to course 1, section 2
    section_assignment2 = SectionAssignment.objects.create(
        COURSE_ASSIGNMENT=course_assignment_1,
        SECTION=section_2
    )

    # Assign a TA to course 3, section 3
    section_assignment3 = SectionAssignment.objects.create(
        COURSE_ASSIGNMENT=course_assignment_3,
        SECTION=section_3
    )


def delete_user(first_name, last_name):
    # Find the instructor you want to delete
    user = User.objects.filter(FIRST_NAME=first_name, LAST_NAME=last_name).first()

    if user:
        # Delete the instructor
        user.delete()


if __name__ == '__main__':
    reset_app('TA_Scheduling_App')
    insert_data()

    # For testing
    # delete_user('Alice', 'Smith')
    # delete_user('Sophia', 'Williams')
