import os
import django
import unittest
import datetime
from unittest.mock import MagicMock

# Set up the Django settings module for testing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TA_Scheduling_Project.settings')
django.setup()

from TA_Scheduling_App.models import Course, Section, User


class TestSetSectionNumber(unittest.TestCase):
    def setUp(self):
        # Mock a course
        self.course = MagicMock(spec=Course)
        self.course.pk = 1

        # Create valid sections
        self.section_1 = Section(SECTION_NUMBER=901, COURSE=self.course, BUILDING='Chemistry Building',
                                 ROOM_NUMBER='190', SECTION_START=datetime.time(9, 30), SECTION_END=datetime.time(10, 20))

        self.section_2 = Section(SECTION_NUMBER=201, COURSE=self.course, BUILDING='Chemistry Building',
                                ROOM_NUMBER='199', SECTION_START=datetime.time(9, 30),
                                SECTION_END=datetime.time(10, 20))

    def test_setSectionNumber_valid(self):
        self.assertTrue(self.section_1.setSectionNumber(801), "Valid section number failed to be set ")

    def test_setSectionNumber_invalid_letters(self):
        self.assertFalse(self.section_1.setSectionNumber("abc"), "Invalid section number was incorrectly set (letters)")

    def test_setSectionNumber_invalid_special_characters(self):
        self.assertFalse(self.section_1.setSectionNumber("#$%^&*"), "Invalid section number was incorrectly set ("
                                                                  "special characters)")

    def test_setSectionNumber_invalid_negative(self):
        self.assertFalse(self.section_1.setSectionNumber(-752), "Invalid section number was incorrectly set (negative)")

    def test_setSectionNumber_empty(self):
        self.assertFalse(self.section_1.setSectionNumber(""), "Empty section number was incorrectly set")

    def test_setSectionNumber_empty_whitespace(self):
        self.assertFalse(self.section_1.setSectionNumber("     "), "Empty section number was incorrectly set")

    def test_setSectionNumber_invalid_null(self):
        self.assertFalse(self.section_1.setSectionNumber(None), "Null section number was incorrectly set ")

    def test_setSectionNumber_existing_section(self):
        self.assertTrue(self.section_1.setSectionNumber(301), "Valid section number failed to be set ")
        self.assertFalse(self.section_2.setSectionNumber(301), "Section number was incorrectly set, the number "
                                                              "is already in use within the same course")

    def test_setSectionNumber_valid_zero(self):
        self.assertTrue(self.section_1.setSectionNumber(0), "Valid section number (0) failed to be set")

    def test_setSectionNumber_invalid_float(self):
        self.assertFalse(self.section_1.setSectionNumber(123.45), "Invalid section number was incorrectly set (float)")

    def test_setSectionNumber_valid_large_number(self):
        self.assertFalse(self.section_1.setSectionNumber(10000), "Section number was set above max value")

class TestSetBuilding(unittest.TestCase):
    def setUp(self):
        # Mock a course
        self.course = MagicMock(spec=Course)
        self.course.pk = 1

        # Create valid sections
        self.section_1 = Section(SECTION_NUMBER=901, COURSE=self.course, BUILDING='Chemistry Building',
                                    ROOM_NUMBER='190', SECTION_START=datetime.time(9, 30), SECTION_END=datetime.time(10, 20))

    def test_setBuilding_valid_with_spaces(self):
        self.assertTrue(self.section_1.setBuilding("Physics Building 2"), "Valid building name with spaces failed to be set.")

    def test_setBuilding_valid_with_hyphen(self):
        self.assertTrue(self.section_1.setBuilding("Physics-Building"), "Valid building name with hyphen failed to be set.")

    def test_setBuilding_valid_with_apostrophe(self):
        self.assertTrue(self.section_1.setBuilding("Physics' Building"), "Valid building name with apostrophe failed to be set.")

    def test_setBuilding_invalid_empty_string(self):
        self.assertFalse(self.section_1.setBuilding(""), "Empty building name was incorrectly set.")

    def test_setBuilding_invalid_whitespace(self):
        self.assertFalse(self.section_1.setBuilding("   "), "Building name with only whitespace was incorrectly set.")

    def test_setBuilding_invalid_special_characters(self):
        self.assertFalse(self.section_1.setBuilding("#$%@"), "Building name with special characters was incorrectly set.")

    def test_setBuilding_valid_unicode(self):
        self.assertTrue(self.section_1.setBuilding("École"), "Valid building name with unicode characters failed to be set.")

    def test_setBuilding_valid_mixed_case(self):
        self.assertTrue(self.section_1.setBuilding("PhYsIcS BuIlDiNg"), "Valid building name with mixed case failed to be set.")

    def test_setBuilding_invalid_spaces_before_after(self):
        self.assertFalse(self.section_1.setBuilding("  Physics Building  "),
                        "Invalid building name with spaces before and after set.")

    def test_setBuilding_invalid_only_numbers(self):
        self.assertFalse(self.section_1.setBuilding("1234"), "Building name with only numbers was incorrectly set.")

    def test_setBuilding_invalid_long_string(self):
        self.assertFalse(self.section_1.setBuilding("a" * 256), "Building name that is too long was incorrectly set.")

    def test_setBuilding_valid_one_letter(self):
        self.assertTrue(self.section_1.setBuilding("P"), "Valid building name with only one letter failed to be set.")

    def test_setBuilding_invalid_null(self):
        self.assertFalse(self.section_1.setBuilding(None), "Null building name was incorrectly set.")

class TestSetRoomNumber(unittest.TestCase):
    def setUp(self):
        # Mock a course
        self.course = MagicMock(spec=Course)
        self.course.pk = 1

        # Create valid section
        self.section = Section(SECTION_NUMBER=901, COURSE=self.course, BUILDING='Chemistry Building',
                               ROOM_NUMBER='190', SECTION_START=datetime.time(9, 30), SECTION_END=datetime.time(10, 20))
    
    def test_setRoomNumber_valid(self):
        self.assertTrue(self.section.setRoomNumber("108"), "Valid room number failed to be set ")

    def test_setRoomNumber_valid_letter(self):
        self.assertTrue(self.section.setRoomNumber("E190"), "Valid room number failed to be set ")
    
    def test_setRoomNumber_valid_mixed_case(self):
        self.assertTrue(self.section.setRoomNumber("aBc123"), "Valid room number with mixed case failed to be set.")

    def test_setRoomNumber_invalid_spaces_before_after(self):
        self.assertFalse(self.section.setRoomNumber(" B101 "), "Invalid room number with spaces before and after set.")
    
    def test_setRoomNumber_valid_length_edge(self):
        self.assertTrue(self.section.setRoomNumber("5" * 10), "Valid room number failed to be set ")

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
        # Mock a course
        self.course = MagicMock(spec=Course)
        self.course.pk = 1

        # Create valid section
        self.section = Section(SECTION_NUMBER=901, COURSE=self.course, BUILDING='Chemistry Building',
                                ROOM_NUMBER='190', SECTION_START=datetime.time(9, 30), SECTION_END=datetime.time(10, 20))

    def test_setSectionStart_valid(self):
        self.assertTrue(self.section.setSectionStart(datetime.time(6, 30)), "Valid start time failed to be set ")

    def test_setSectionStart_max_time(self):
        self.assertTrue(self.section.setSectionStart(datetime.time(23, 59)), "Valid start time failed to be set on "
                                                                             "maximum time value")

    def test_setSectionStart_min_time(self):
        self.assertTrue(self.section.setSectionStart(datetime.time(0, 0)), "Valid start time failed to be set on "
                                                                           "minimum time value (midnight)")

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
        # Mock a course
        self.course = MagicMock(spec=Course)
        self.course.pk = 1

        # Create valid section
        self.section = Section(SECTION_NUMBER=901, COURSE=self.course, BUILDING='Chemistry Building',
                                ROOM_NUMBER='190', SECTION_START=datetime.time(9, 30), SECTION_END=datetime.time(10, 20))

    def test_setSectionEnd_valid(self):
        self.assertTrue(self.section.setSectionEnd(datetime.time(10, 30)), "Valid end time failed to be set ")

    def test_setSectionEnd_max_time(self):
        self.assertTrue(self.section.setSectionEnd(datetime.time(23, 59)), "Valid end time failed to be set on "
                                                                           "maximum time value")

    def test_setSectionEnd_min_time(self):
        self.assertTrue(self.section.setSectionEnd(datetime.time(0, 0)), "Valid end time failed to be set on "
                                                                         "minimum time value (midnight)")

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
