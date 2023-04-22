import os
import django
import unittest
import datetime

# Set up the Django settings module for testing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TA_Scheduling_Project.settings')
django.setup()

from TA_Scheduling_App.models import Course, Section, User


class TestSetSectionNumber(unittest.TestCase):
    def setUp(self):
        self.instructor = User(ROLL='INSTRUCTOR', FIRST_NAME='Jane', LAST_NAME='Doe', EMAIL='jane.doe@example.com',
                               PHONE_NUMBER='555-123-4567', ADDRESS='1234 Elm St', BIRTH_DATE='1995-08-30')
        self.course = Course(COURSE_NUMBER=361, INSTRUCTOR=self.instructor, COURSE_NAME='Intro to SE',
                             COURSE_DESCRIPTION='This course serves as an introduction to software engineering.',
                             SEMESTER='Summer 2023',
                             PREREQUISITES='None', DEPARTMENT='Applied Mathematics and Computer Science Program')

        self.section = Section(SECTION_NUMBER=901, COURSE=self.course, BUILDING='Chemistry Building',
                               ROOM_NUMBER='190', SECTION_START=datetime.time(9, 30), SECTION_END=datetime.time(10, 20))

        self.section2 = Section(SECTION_NUMBER=201, COURSE=self.course, BUILDING='Chemistry Building',
                                ROOM_NUMBER='199', SECTION_START=datetime.time(9, 30),
                                SECTION_END=datetime.time(10, 20))

    def test_setSectionNumber_valid(self):
        self.assertTrue(self.section.setSectionNumber(801), "Valid section number failed to be set ")
        self.assertEqual(self.section.SECTION_NUMBER, 801, "Section number was set to incorrect value")

    def test_setSectionNumber_invalid_letters(self):
        self.assertFalse(self.section.setSectionNumber("abc"), "Invalid section number was incorrectly set (letters)")

    def test_setSectionNumber_invalid_special_characters(self):
        self.assertFalse(self.section.setSectionNumber("#$%^&*"), "Invalid section number was incorrectly set ("
                                                                  "special characters)")

    def test_setSectionNumber_invalid_negative(self):
        self.assertFalse(self.section.setSectionNumber(-752), "Invalid section number was incorrectly set (negative)")

    def test_setSectionNumber_empty(self):
        self.assertFalse(self.section.setSectionNumber(""), "Empty section number was incorrectly set")

    def test_setSectionNumber_empty_whitespace(self):
        self.assertFalse(self.section.setSectionNumber("     "), "Empty section number was incorrectly set")

    def test_setSectionNumber_invalid_null(self):
        self.assertFalse(self.section.setSectionNumber(None), "Null section number was incorrectly set ")

    def test_setSectionNumber_existing_section(self):
        self.assertTrue(self.section.setSectionNumber(301), "Valid section number failed to be set ")
        self.assertFalse(self.section2.setSectionNumber(301), "Section number was incorrectly set, the number "
                                                              "is already in use within the same course")


class TestSetBuilding(unittest.TestCase):
    def setUp(self):
        self.instructor = User(ROLL='INSTRUCTOR', FIRST_NAME='Jane', LAST_NAME='Doe', EMAIL='jane.doe@example.com',
                               PHONE_NUMBER='555-123-4567', ADDRESS='1234 Elm St', BIRTH_DATE='1995-08-30')
        self.course = Course(COURSE_NUMBER=361, INSTRUCTOR=self.instructor, COURSE_NAME='Intro to SE',
                             COURSE_DESCRIPTION='This course serves as an introduction to software engineering.',
                             SEMESTER='Summer 2023',
                             PREREQUISITES='None', DEPARTMENT='Applied Mathematics and Computer Science Program')

        self.section = Section(SECTION_NUMBER=901, COURSE=self.course, BUILDING='Chemistry Building',
                               ROOM_NUMBER='190', SECTION_START=datetime.time(9, 30), SECTION_END=datetime.time(10, 20))

    def test_setBuilding_valid(self):
        self.assertTrue(self.section.setBuilding("EMS"), "Valid building name failed to be set ")
        self.assertEqual(self.section.BUILDING, "EMS", "Building name was set to incorrect value")

    def test_setBuilding_empty(self):
        self.assertFalse(self.section.setBuilding(""), "Empty building name was incorrectly set")

    def test_setBuilding_empty_whitespace(self):
        self.assertFalse(self.section.setBuilding("     "), "Empty building name was incorrectly set")

    def test_setBuilding_long_string(self):
        self.assertFalse(self.section.setBuilding("a" * 256), "Building name that was too long was incorrectly "
                                                              "set")

    def test_setBuilding_invalid_null(self):
        self.assertFalse(self.section.setBuilding(None), "Null building name was incorrectly set ")

    def test_setBuilding_valid_length_edge(self):
        self.assertTrue(self.section.setBuilding("b" * 255), "Valid building name failed to be set ")
        self.assertEqual(self.section.BUILDING, "b" * 255, "Building name was set to incorrect value")


class TestSetRoomNumber(unittest.TestCase):
    def setUp(self):
        self.instructor = User(ROLL='INSTRUCTOR', FIRST_NAME='Jane', LAST_NAME='Doe', EMAIL='jane.doe@example.com',
                               PHONE_NUMBER='555-123-4567', ADDRESS='1234 Elm St', BIRTH_DATE='1995-08-30')
        self.course = Course(COURSE_NUMBER=361, INSTRUCTOR=self.instructor, COURSE_NAME='Intro to SE',
                             COURSE_DESCRIPTION='This course serves as an introduction to software engineering.',
                             SEMESTER='Summer 2023',
                             PREREQUISITES='None', DEPARTMENT='Applied Mathematics and Computer Science Program')

        self.section = Section(SECTION_NUMBER=901, COURSE=self.course, BUILDING='Chemistry Building',
                               ROOM_NUMBER='190', SECTION_START=datetime.time(9, 30), SECTION_END=datetime.time(10, 20))

    def test_setRoomNumber_valid(self):
        self.assertTrue(self.section.setRoomNumber("108"), "Valid room number failed to be set ")
        self.assertEqual(self.section.ROOM_NUMBER, "108", "Room number was set to incorrect value")

    def test_setRoomNumber_valid_letter(self):
        self.assertTrue(self.section.setRoomNumber("E190"), "Valid room number failed to be set ")
        self.assertEqual(self.section.ROOM_NUMBER, "E190", "Room number was set to incorrect value")

    def test_setRoomNumber_valid_length_edge(self):
        self.assertTrue(self.section.setRoomNumber("5" * 10), "Valid room number failed to be set ")
        self.assertEqual(self.section.ROOM_NUMBER, "5" * 10, "Room number was set to incorrect value")

    def test_setRoomNumber_invalid_special_characters(self):
        self.assertFalse(self.section.setRoomNumber("$%^&"), "Invalid room number was incorrectly set (special "
                                                             "characters)")

    def test_setBuilding_empty_whitespace(self):
        self.assertFalse(self.section.setRoomNumber("     "), "Empty room number was incorrectly set")

    def test_setRoomNumber_invalid_empty(self):
        self.assertFalse(self.section.setRoomNumber(""), "Empty room number was incorrectly set")

    def test_setRoomNumber_invalid_null(self):
        self.assertFalse(self.section.setRoomNumber(None), "Null room number was incorrectly set")

    def test_setRoomNumber_invalid_too_long(self):
        self.assertFalse(self.section.setRoomNumber("5" * 11), "Room number that was too long was incorrectly set")


class TestSetSectionStart(unittest.TestCase):
    def setUp(self):
        self.instructor = User(ROLL='INSTRUCTOR', FIRST_NAME='Jane', LAST_NAME='Doe', EMAIL='jane.doe@example.com',
                               PHONE_NUMBER='555-123-4567', ADDRESS='1234 Elm St', BIRTH_DATE='1995-08-30')
        self.course = Course(COURSE_NUMBER=361, INSTRUCTOR=self.instructor, COURSE_NAME='Intro to SE',
                             COURSE_DESCRIPTION='This course serves as an introduction to software engineering.',
                             SEMESTER='Summer 2023',
                             PREREQUISITES='None', DEPARTMENT='Applied Mathematics and Computer Science Program')

        self.section = Section(SECTION_NUMBER=901, COURSE=self.course, BUILDING='Chemistry Building',
                               ROOM_NUMBER='190', SECTION_START=datetime.time(9, 30), SECTION_END=datetime.time(11, 20))

    def test_setSectionStart_valid(self):
        self.assertTrue(self.section.setSectionStart(datetime.time(6, 30)), "Valid start time failed to be set ")
        self.assertEqual(self.section.SECTION_START, datetime.time(6, 30), "Section start time was set to incorrect "
                                                                           "value")

    def test_setSectionStart_max_time(self):
        self.assertTrue(self.section.setSectionStart(datetime.time(23, 59)), "Valid start time failed to be set on "
                                                                             "maximum time value")
        self.assertEqual(self.section.SECTION_START, datetime.time(23, 59), "Section start time was set to incorrect "
                                                                            "value")

    def test_setSectionStart_min_time(self):
        self.assertTrue(self.section.setSectionStart(datetime.time(0, 0)), "Valid start time failed to be set on "
                                                                           "minimum time value (midnight)")
        self.assertEqual(self.section.SECTION_START, datetime.time(0, 0), "Section start time was set to incorrect "
                                                                          "value")

    def test_setSectionStart_invalid_null(self):
        self.assertFalse(self.section.setSectionStart(None), "Null section start time was incorrectly set")

    def test_setSectionStart_invalid_nonexistent(self):
        with self.assertRaises(ValueError):
            self.section.setSectionStart(datetime.time(29, 30))
            self.fail("Allowed setting section start time with time out of range")

    def test_setSectionStart_invalid_negative(self):
        with self.assertRaises(ValueError):
            self.section.setSectionStart(datetime.time(-10, 30))
            self.fail("Allowed setting section start time with negative time")

    def test_setSectionStart_invalid_string(self):
        self.assertFalse(self.section.setSectionStart("10:30"), "Section start time was incorrectly set, cannot be "
                                                                "string")


class TestSetSectionEnd(unittest.TestCase):
    def setUp(self):
        self.instructor = User(ROLL='INSTRUCTOR', FIRST_NAME='Jane', LAST_NAME='Doe', EMAIL='jane.doe@example.com',
                               PHONE_NUMBER='555-123-4567', ADDRESS='1234 Elm St', BIRTH_DATE='1995-08-30')
        self.course = Course(COURSE_NUMBER=361, INSTRUCTOR=self.instructor, COURSE_NAME='Intro to SE',
                             COURSE_DESCRIPTION='This course serves as an introduction to software engineering.',
                             SEMESTER='Summer 2023',
                             PREREQUISITES='None', DEPARTMENT='Applied Mathematics and Computer Science Program')

        self.section = Section(SECTION_NUMBER=901, COURSE=self.course, BUILDING='Chemistry Building',
                               ROOM_NUMBER='190', SECTION_START=datetime.time(9, 30), SECTION_END=datetime.time(11, 20))

    def test_setSectionEnd_valid(self):
        self.assertTrue(self.section.setSectionEnd(datetime.time(10, 30)), "Valid end time failed to be set ")
        self.assertEqual(self.section.SECTION_END, datetime.time(10, 30), "Section end time was set to incorrect "
                                                                         "value")

    def test_setSectionEnd_max_time(self):
        self.assertTrue(self.section.setSectionEnd(datetime.time(23, 59)), "Valid end time failed to be set on "
                                                                           "maximum time value")
        self.assertEqual(self.section.SECTION_END, datetime.time(23, 59), "Section end time was set to incorrect "
                                                                          "value")

    def test_setSectionEnd_min_time(self):
        self.assertTrue(self.section.setSectionEnd(datetime.time(0, 0)), "Valid end time failed to be set on "
                                                                         "minimum time value (midnight)")
        self.assertEqual(self.section.SECTION_END, datetime.time(0, 0), "Section end time was set to incorrect "
                                                                        "value")

    def test_setSectionEnd_invalid_null(self):
        self.assertFalse(self.section.setSectionEnd(None), "Null section end time was incorrectly set")

    def test_setSectionEnd_invalid_nonexistent(self):
        with self.assertRaises(ValueError):
            self.section.setSectionEnd(datetime.time(35, 30))
            self.fail("Allowed setting section end time with time out of range")

    def test_setSectionEnd_invalid_negative(self):
        with self.assertRaises(ValueError):
            self.section.setSectionEnd(datetime.time(-11, 30))
            self.fail("Allowed setting section end time with negative time")

    def test_setSectionEnd_invalid_string(self):
        self.assertFalse(self.section.setSectionEnd("11:30"), "Section end time was incorrectly set, cannot be "
                                                              "string")

    def test_setSectionEnd_before_start(self):
        self.assertFalse(self.section.setSectionEnd(datetime.time(9, 30)), "Section end time was incorrectly set, "
                                                                           "cannot be at start time")

    def test_setSectionEnd_at_start(self):
        self.assertFalse(self.section.setSectionEnd(datetime.time(8, 30)), "Section end time was incorrectly set, "
                                                                           "cannot be before start time")
