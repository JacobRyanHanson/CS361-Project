import os
import django
import unittest
import datetime
from unittest.mock import MagicMock, patch

# Set up the Django settings module for testing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TA_Scheduling_Project.settings')
django.setup()

from TA_Scheduling_App.models import Course, Section, User

class TestSectionInit(unittest.TestCase):
    def setUp(self):
        # Mock a course
        self.course = MagicMock(spec=Course)
        self.course.pk = 1
        self.course._state = MagicMock()
        self.course._state.db = 'default'

    def test_init_valid_input(self):
        try:
            # Mock the checkDuplicate method for the instantiation, so we don't actually access the DB
            with patch.object(Section, 'checkDuplicate', return_value=False):
                Section(SECTION_TYPE="LAB",
                        SECTION_NUMBER=901,
                        COURSE=self.course,
                        BUILDING='Chemistry Building',
                        ROOM_NUMBER='190',
                        SECTION_START=datetime.time(9, 30),
                        SECTION_END=datetime.time(10, 20))
        except ValueError:
            self.fail("Section init failed with valid input values.")

    def test_init_invalid_course(self):
        with self.assertRaises(ValueError, msg="Section init did not raise ValueError for invalid COURSE"):
            # Mock the checkDuplicate method for the instantiation, so we don't actually access the DB
            with patch.object(Section, 'checkDuplicate', return_value=False):
                Section(SECTION_TYPE="LAB",
                        SECTION_NUMBER=901,
                        COURSE=None,
                        BUILDING='Chemistry Building',
                        ROOM_NUMBER='190',
                        SECTION_START=datetime.time(9, 30),
                        SECTION_END=datetime.time(10, 20))

#     Please note setters will handle all additional checking on initialization.


class TestSetSectionType(unittest.TestCase):
    def setUp(self):
        # Mock a course
        self.course = MagicMock(spec=Course)
        self.course.pk = 1
        self.course._state = MagicMock()
        self.course._state.db = 'default'

        # Mock the checkDuplicate method for the instantiation, so we don't actually access the DB
        with patch.object(Section, 'checkDuplicate', return_value=False):
            # Create valid section
            self.section = Section(
                SECTION_TYPE="LAB",
                SECTION_NUMBER=901,
                COURSE=self.course,
                BUILDING='Chemistry Building',
                ROOM_NUMBER='190',
                SECTION_START=datetime.time(9, 30),
                SECTION_END=datetime.time(10, 20))

    def test_setSectionType_valid_Lab(self):
        self.assertTrue(self.section.setSectionType("LAB"), "Valid section type 'LAB' failed to be set.")

    def test_setSectionType_valid_Lecture(self):
        self.assertTrue(self.section.setSectionType("LECTURE"), "Valid section type 'LECTURE' failed to be set.")

    def test_setSectionType_invalid_empty_string(self):
        self.assertFalse(self.section.setSectionType(""), "Empty section type string was incorrectly set.")

    def test_setSectionType_invalid_whitespace(self):
        self.assertFalse(self.section.setSectionType("   "), "Section type with only whitespace was incorrectly set.")

    def test_setSectionType_invalid_lowercase(self):
        self.assertFalse(self.section.setSectionType("lab"), "Lowercase section type string was incorrectly set.")

    def test_setSectionType_invalid_mixed_case(self):
        self.assertFalse(self.section.setSectionType("LaB"), "Mixed case section type string was incorrectly set.")

    def test_setSectionType_invalid_numbers(self):
        self.assertFalse(self.section.setSectionType("1234"), "Section type with numbers was incorrectly set.")

    def test_setSectionType_invalid_special_characters(self):
        self.assertFalse(self.section.setSectionType("#$%@"), "Section type with special characters was incorrectly set.")

    def test_setSectionType_invalid_other_string(self):
        self.assertFalse(self.section.setSectionType("LUNCH"), "Invalid section type string was incorrectly set.")

    def test_setSectionType_invalid_spaces_before_after(self):
        self.assertFalse(self.section.setSectionType("  LAB  "), "Section type with spaces before and after was incorrectly set.")

    def test_setSectionType_invalid_combination(self):
        self.assertFalse(self.section.setSectionType("LAB123"), "Section type with letters and numbers was incorrectly set.")

    def test_setSectionType_invalid_unicode(self):
        self.assertFalse(self.section.setSectionType("LÄB"), "Section type with unicode characters was incorrectly set.")

    def test_setSectionType_invalid_long_string(self):
        self.assertFalse(self.section.setSectionType("A" * 256), "Section type with too long string was incorrectly set.")

    def test_setSectionType_invalid_one_letter(self):
        self.assertFalse(self.section.setSectionType("A"), "Section type with only one letter was incorrectly set.")

    def test_setSectionType_invalid_null(self):
        self.assertFalse(self.section.setSectionType(None), "Null section type was incorrectly set.")

class TestSetSectionNumber(unittest.TestCase):
    def setUp(self):
        # Mock a course
        self.course = MagicMock(spec=Course)
        self.course.pk = 1
        self.course._state = MagicMock()
        self.course._state.db = 'default'

        # Mock the checkDuplicate method for the instantiation, so we don't actually access the DB
        with patch.object(Section, 'checkDuplicate', return_value=False):
            # Create valid section
            self.section = Section(
                SECTION_TYPE="LAB",
                SECTION_NUMBER=901,
                COURSE=self.course,
                BUILDING='Chemistry Building',
                ROOM_NUMBER='190',
                SECTION_START=datetime.time(9, 30),
                SECTION_END=datetime.time(10, 20))


    def test_setSectionNumber_valid(self):
        with patch.object(self.section, 'checkDuplicate', return_value=False):
            self.assertTrue(self.section.setSectionNumber(801), "Valid section number failed to be set ")

    def test_setSectionNumber_invalid_letters(self):
        with patch.object(self.section, 'checkDuplicate', return_value=False):
            self.assertFalse(self.section.setSectionNumber("abc"), "Invalid section number was incorrectly set (letters)")

    def test_setSectionNumber_invalid_special_characters(self):
        with patch.object(self.section, 'checkDuplicate', return_value=False):
            self.assertFalse(self.section.setSectionNumber("#$%^&*"), "Invalid section number was incorrectly set ("
                                                                  "special characters)")

    def test_setSectionNumber_invalid_negative(self):
        with patch.object(self.section, 'checkDuplicate', return_value=False):
            self.assertFalse(self.section.setSectionNumber(-752), "Invalid section number was incorrectly set (negative)")

    def test_setSectionNumber_empty(self):
        with patch.object(self.section, 'checkDuplicate', return_value=False):
            self.assertFalse(self.section.setSectionNumber(""), "Empty section number was incorrectly set")

    def test_setSectionNumber_empty_whitespace(self):
        with patch.object(self.section, 'checkDuplicate', return_value=False):
            self.assertFalse(self.section.setSectionNumber("     "), "Empty section number was incorrectly set")

    def test_setSectionNumber_invalid_null(self):
        with patch.object(self.section, 'checkDuplicate', return_value=False):
            self.assertFalse(self.section.setSectionNumber(None), "Null section number was incorrectly set ")

    def test_setSectionNumber_valid_zero(self):
        with patch.object(self.section, 'checkDuplicate', return_value=False):
            self.assertTrue(self.section.setSectionNumber(0), "Valid section number (0) failed to be set")

    def test_setSectionNumber_invalid_float(self):
        with patch.object(self.section, 'checkDuplicate', return_value=False):
            self.assertFalse(self.section.setSectionNumber(123.45), "Invalid section number was incorrectly set (float)")

    def test_setSectionNumber_valid_large_number(self):
        with patch.object(self.section, 'checkDuplicate', return_value=False):
            self.assertFalse(self.section.setSectionNumber(10000), "Section number was set above max value")

class TestSetBuilding(unittest.TestCase):
    def setUp(self):
        # Mock a course
        self.course = MagicMock(spec=Course)
        self.course.pk = 1
        self.course._state = MagicMock()
        self.course._state.db = 'default'

        # Mock the checkDuplicate method for the instantiation, so we don't actually access the DB
        with patch.object(Section, 'checkDuplicate', return_value=False):
            # Create valid section
            self.section = Section(
                SECTION_TYPE="LAB",
                SECTION_NUMBER=901,
                COURSE=self.course,
                BUILDING='Chemistry Building',
                ROOM_NUMBER='190',
                SECTION_START=datetime.time(9, 30),
                SECTION_END=datetime.time(10, 20))

    def test_setBuilding_valid_with_spaces(self):
        self.assertTrue(self.section.setBuilding("Physics Building 2"), "Valid building name with spaces failed to be set.")

    def test_setBuilding_valid_with_hyphen(self):
        self.assertTrue(self.section.setBuilding("Physics-Building"), "Valid building name with hyphen failed to be set.")

    def test_setBuilding_valid_with_apostrophe(self):
        self.assertTrue(self.section.setBuilding("Physics' Building"), "Valid building name with apostrophe failed to be set.")

    def test_setBuilding_invalid_empty_string(self):
        self.assertFalse(self.section.setBuilding(""), "Empty building name was incorrectly set.")

    def test_setBuilding_invalid_whitespace(self):
        self.assertFalse(self.section.setBuilding("   "), "Building name with only whitespace was incorrectly set.")

    def test_setBuilding_invalid_special_characters(self):
        self.assertFalse(self.section.setBuilding("#$%@"), "Building name with special characters was incorrectly set.")

    def test_setBuilding_invalid_unicode(self):
        self.assertFalse(self.section.setBuilding("École"), "Invalid building name with unicode characters set.")

    def test_setBuilding_valid_mixed_case(self):
        self.assertTrue(self.section.setBuilding("PhYsIcS BuIlDiNg"), "Valid building name with mixed case failed to be set.")

    def test_setBuilding_valid_spaces_before_after(self):
        self.assertTrue(self.section.setBuilding("  Physics Building  "),
                        "Valid building name with spaces before and after failed to be set.")

    def test_setBuilding_invalid_only_numbers(self):
        self.assertFalse(self.section.setBuilding("1234"), "Building name with only numbers was incorrectly set.")

    def test_setBuilding_invalid_long_string(self):
        self.assertFalse(self.section.setBuilding("a" * 256), "Building name that is too long was incorrectly set.")

    def test_setBuilding_valid_one_letter(self):
        self.assertTrue(self.section.setBuilding("P"), "Valid building name with only one letter failed to be set.")

    def test_setBuilding_invalid_null(self):
        self.assertFalse(self.section.setBuilding(None), "Null building name was incorrectly set.")

class TestSetRoomNumber(unittest.TestCase):
    def setUp(self):
        # Mock a course
        self.course = MagicMock(spec=Course)
        self.course.pk = 1
        self.course._state = MagicMock()
        self.course._state.db = 'default'

        # Mock the checkDuplicate method for the instantiation, so we don't actually access the DB
        with patch.object(Section, 'checkDuplicate', return_value=False):
            # Create valid section
            self.section = Section(
                SECTION_TYPE="LAB",
                SECTION_NUMBER=901,
                COURSE=self.course,
                BUILDING='Chemistry Building',
                ROOM_NUMBER='190',
                SECTION_START=datetime.time(9, 30),
                SECTION_END=datetime.time(10, 20))
    
    def test_setRoomNumber_valid(self):
        self.assertTrue(self.section.setRoomNumber("108"), "Valid room number failed to be set ")

    def test_setRoomNumber_valid_letter(self):
        self.assertTrue(self.section.setRoomNumber("E190"), "Valid room number failed to be set ")
    
    def test_setRoomNumber_valid_mixed_case(self):
        self.assertTrue(self.section.setRoomNumber("aBc123"), "Valid room number with mixed case failed to be set.")

    def test_setRoomNumber_valid_spaces_before_after(self):
        self.assertTrue(self.section.setRoomNumber(" B101 "), "Valid room number with spaces before and after failed to be set.")
    
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
        self.course._state = MagicMock()
        self.course._state.db = 'default'

        # Mock the checkDuplicate method for the instantiation, so we don't actually access the DB
        with patch.object(Section, 'checkDuplicate', return_value=False):
            # Create valid section
            self.section = Section(
                SECTION_TYPE="LAB",
                SECTION_NUMBER=901,
                COURSE=self.course,
                BUILDING='Chemistry Building',
                ROOM_NUMBER='190',
                SECTION_START=datetime.time(9, 30),
                SECTION_END=datetime.time(10, 20))

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
        self.course._state = MagicMock()
        self.course._state.db = 'default'

        # Mock the checkDuplicate method for the instantiation, so we don't actually access the DB
        with patch.object(Section, 'checkDuplicate', return_value=False):
            # Create valid section
            self.section = Section(
                SECTION_TYPE="LAB",
                SECTION_NUMBER=901,
                COURSE=self.course,
                BUILDING='Chemistry Building',
                ROOM_NUMBER='190',
                SECTION_START=datetime.time(9, 30),
                SECTION_END=datetime.time(10, 20))

    def test_setSectionEnd_valid(self):
        self.assertTrue(self.section.setSectionEnd(datetime.time(10, 30)), "Valid end time failed to be set ")

    def test_setSectionEnd_max_time(self):
        self.assertTrue(self.section.setSectionEnd(datetime.time(23, 59)), "Valid end time failed to be set on "
                                                                           "maximum time value")

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
