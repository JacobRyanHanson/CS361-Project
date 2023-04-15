import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TA_Scheduling_Project.settings')
django.setup()

from TA_Scheduling_App.models.User import User
from TA_Scheduling_App.models.Course import Course
from TA_Scheduling_App.models.Section import Section
from TA_Scheduling_App.models.TA_Assignment import TAAssignment
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
    user1 = User.objects.create(
        USER_TYPE='ADMIN',
        FIRST_NAME='John',
        LAST_NAME='Doe',
        EMAIL='john.doe@example.com',
        PASSWORD_HASH='<hashed_password>',
        PHONE_NUMBER='555-123-4567',
        ADDRESS='123 Main St',
        BIRTH_DATE=date(1990, 1, 1)
    )

    user2 = User.objects.create(
        USER_TYPE='INSTRUCTOR',
        FIRST_NAME='Alice',
        LAST_NAME='Smith',
        EMAIL='alice.smith@example.com',
        PASSWORD_HASH='<hashed_password>',
        PHONE_NUMBER='555-987-6543',
        ADDRESS='456 Elm St',
        BIRTH_DATE=date(1985, 6, 15)
    )

    user3 = User.objects.create(
        USER_TYPE='ADMIN',
        FIRST_NAME='Emma',
        LAST_NAME='Johnson',
        EMAIL='emma.johnson@example.com',
        PASSWORD_HASH='<hashed_password>',
        PHONE_NUMBER='555-123-4587',
        ADDRESS='789 Oak St',
        BIRTH_DATE=date(1992, 3, 12)
    )

    user4 = User.objects.create(
        USER_TYPE='INSTRUCTOR',
        FIRST_NAME='Michael',
        LAST_NAME='Brown',
        EMAIL='michael.brown@example.com',
        PASSWORD_HASH='<hashed_password>',
        PHONE_NUMBER='555-987-6578',
        ADDRESS='321 Pine St',
        BIRTH_DATE=date(1988, 10, 20)
    )

    user5 = User.objects.create(
        USER_TYPE='TA',
        FIRST_NAME='Sophia',
        LAST_NAME='Williams',
        EMAIL='sophia.williams@example.com',
        PASSWORD_HASH='<hashed_password>',
        PHONE_NUMBER='555-123-4599',
        ADDRESS='147 Maple St',
        BIRTH_DATE=date(1994, 7, 25)
    )

    # Insert courses
    course1 = Course.objects.create(
        COURSE_NUMBER=101,
        INSTRUCTOR=user2,
        COURSE_NAME='Introduction to Computer Science',
        COURSE_DESCRIPTION='An introductory course to the world of computer science.',
        SEMESTER='Fall 2023',
        PREREQUISITES='',
        DEPARTMENT='Computer Science'
    )

    course2 = Course.objects.create(
        COURSE_NUMBER=102,
        INSTRUCTOR=user2,
        COURSE_NAME='Data Structures',
        COURSE_DESCRIPTION='A course on fundamental data structures in computer science.',
        SEMESTER='Spring 2023',
        PREREQUISITES='Introduction to Computer Science',
        DEPARTMENT='Computer Science'
    )

    course3 = Course.objects.create(
        COURSE_NUMBER=103,
        INSTRUCTOR=user4,
        COURSE_NAME='Algorithms',
        COURSE_DESCRIPTION='A course on fundamental algorithms in computer science.',
        SEMESTER='Fall 2023',
        PREREQUISITES='Data Structures',
        DEPARTMENT='Computer Science'
    )

    course4 = Course.objects.create(
        COURSE_NUMBER=104,
        INSTRUCTOR=user4,
        COURSE_NAME='Operating Systems',
        COURSE_DESCRIPTION='A course on the principles of operating systems.',
        SEMESTER='Spring 2023',
        PREREQUISITES='Data Structures',
        DEPARTMENT='Computer Science'
    )

    # Insert sections
    section1 = Section.objects.create(
        SECTION_NUMBER=1,
        COURSE=course1,
        SECTION_TYPE='LECTURE',
        BUILDING='Tech Building',
        ROOM_NUMBER='101',
        SECTION_START=time(9, 0),
        SECTION_END=time(10, 15)
    )

    section2 = Section.objects.create(
        SECTION_NUMBER=2,
        COURSE=course2,
        SECTION_TYPE='LECTURE',
        BUILDING='Tech Building',
        ROOM_NUMBER='102',
        SECTION_START=time(10, 30),
        SECTION_END=time(11, 45)
    )

    section3 = Section.objects.create(
        SECTION_NUMBER=1,
        COURSE=course3,
        SECTION_TYPE='LECTURE',
        BUILDING='Tech Building',
        ROOM_NUMBER='103',
        SECTION_START=time(12, 0),
        SECTION_END=time(13, 15)
    )

    section4 = Section.objects.create(
        SECTION_NUMBER=2,
        COURSE=course4,
        SECTION_TYPE='LECTURE',
        BUILDING='Tech Building',
        ROOM_NUMBER='104',
        SECTION_START=time(14, 0),
        SECTION_END=time(15, 15)
    )

    # Insert TA assignments

    TAAssignment.objects.create(
        COURSE=course1,
        SECTION=section1,
        TA=user5,
        IS_GRADER=False
    )

    TAAssignment.objects.create(
        COURSE=course3,
        SECTION=section3,
        TA=user5,
        IS_GRADER=True
    )


def delete_instructor(first_name, last_name):
    # Find the instructor you want to delete
    instructor = User.objects.filter(FIRST_NAME=first_name, LAST_NAME=last_name).first()

    if instructor:
        # Delete the instructor
        instructor.delete()


if __name__ == '__main__':
    reset_app('TA_Scheduling_App')
    insert_data()
    delete_instructor('Alice', 'Smith')
