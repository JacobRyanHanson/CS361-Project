import os
import django
import unittest
from unittest.mock import MagicMock, patch

# Set up the Django settings module for testing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TA_Scheduling_Project.settings')
django.setup()

from TA_Scheduling_App.models import Course, User

    
class TestCourseInit(unittest.TestCase):
    def test_init_valid_input(self):
        try:
            # Mock the checkDuplicate method for the instantiation, so we don't actually access the DB
            with patch.object(Course, 'checkDuplicate', return_value=False):
                Course(COURSE_NUMBER=101,
                    COURSE_NAME='Advanced Chemistry',
                    COURSE_DESCRIPTION='A study of advanced topics in chemistry.',
                    SEMESTER='Spring 2024',
                    PREREQUISITES='Basic Chemistry',
                    DEPARTMENT='Computer Science')
        except ValueError:
            self.fail("Course init failed with valid input values.")

#     Please note setters will handle all additional checking on initialization.


class TestSetCourseNumber(unittest.TestCase):
    def setUp(self):
        # Mock the checkDuplicate method for the instantiation, so we don't actually access the DB
        with patch.object(Course, 'checkDuplicate', return_value=False):
            # Create Course object with mocked User
            self.course_1 = Course(
                COURSE_NUMBER=901,
                COURSE_NAME='Introduction to Computer Science',
                COURSE_DESCRIPTION='A beginner\'s course in computer science, covering programming fundamentals.',
                SEMESTER='Fall 2023',
                PREREQUISITES='None',
                DEPARTMENT='Computer Science'
            )

    def test_setCourseNumber_valid(self):
        with patch.object(self.course_1, 'checkDuplicate', return_value=False):
            self.assertTrue(self.course_1.setCourseNumber(801), "Valid course number failed to be set ")

    def test_setCourseNumber_invalid_letters(self):
        with patch.object(self.course_1, 'checkDuplicate', return_value=False):
            self.assertFalse(self.course_1.setCourseNumber("abc"), "Invalid course number was incorrectly set (letters)")

    def test_setCourseNumber_invalid_special_characters(self):
        with patch.object(self.course_1, 'checkDuplicate', return_value=False):
            self.assertFalse(self.course_1.setCourseNumber("#$%^&*"), "Invalid course number was incorrectly set ("
                                                                "special characters)")

    def test_setCourseNumber_invalid_negative(self):
        with patch.object(self.course_1, 'checkDuplicate', return_value=False):
            self.assertFalse(self.course_1.setCourseNumber(-752), "Invalid course number was incorrectly set (negative)")

    def test_setCourseNumber_empty(self):
        with patch.object(self.course_1, 'checkDuplicate', return_value=False):
            self.assertFalse(self.course_1.setCourseNumber(""), "Empty course number was incorrectly set")

    def test_setCourseNumber_empty_whitespace(self):
        with patch.object(self.course_1, 'checkDuplicate', return_value=False):
            self.assertFalse(self.course_1.setCourseNumber("     "), "Empty course number was incorrectly set")

    def test_setCourseNumber_invalid_null(self):
        with patch.object(self.course_1, 'checkDuplicate', return_value=False):
            self.assertFalse(self.course_1.setCourseNumber(None), "Null course number was incorrectly set ")

    def test_setCourseNumber_valid_zero(self):
        with patch.object(self.course_1, 'checkDuplicate', return_value=False):
            self.assertTrue(self.course_1.setCourseNumber(0), "Valid course number (0) failed to be set")

    def test_setCourseNumber_invalid_float(self):
        with patch.object(self.course_1, 'checkDuplicate', return_value=False):
            self.assertFalse(self.course_1.setCourseNumber(123.45), "Invalid course number was incorrectly set (float)")

    def test_setCourseNumber_invalid_large_number(self):
        with patch.object(self.course_1, 'checkDuplicate', return_value=False):
            self.assertFalse(self.course_1.setCourseNumber(10000), "Course number was set above max value")


class TestSetCourseName(unittest.TestCase):
    def setUp(self):
        # Mock the checkDuplicate method for the instantiation, so we don't actually access the DB
        with patch.object(Course, 'checkDuplicate', return_value=False):
            # Create Course object with mocked User
            self.course = Course(
                COURSE_NUMBER=101,
                COURSE_NAME='Introduction to Computer Science',
                COURSE_DESCRIPTION='A beginner\'s course in computer science, covering programming fundamentals.',
                SEMESTER='Fall 2023',
                PREREQUISITES='None',
                DEPARTMENT='Computer Science'
            )
    
    def test_setCourseName_valid(self):
        self.assertTrue(self.course.setCourseName("Introduction to Computer Science"),
        "Valid course name failed to be set.")

    def test_setCourseName_valid_with_spaces(self):
        self.assertTrue(self.course.setCourseName("Data Structures and Algorithms"),
        "Valid course name with spaces failed to be set.")

    def test_setCourseName_valid_mixed_case(self):
        self.assertTrue(self.course.setCourseName("inTrOdUctIon tO CoMpUtEr ScIeNcE"),
        "Valid course name with mixed case failed to be set.")

    def test_setCourseName_invalid_empty_string(self):
        self.assertFalse(self.course.setCourseName(""), "Empty course name was incorrectly set.")

    def test_setCourseName_invalid_whitespace(self):
        self.assertFalse(self.course.setCourseName(" "), "Course name with only whitespace was incorrectly set.")

    def test_setCourseName_invalid_special_characters(self):
        self.assertFalse(self.course.setCourseName("#$%@"), "Course name with special characters was incorrectly set.")

    def test_setCourseName_invalid_numbers(self):
        self.assertFalse(self.course.setCourseName("1234"), "Course name with numbers was incorrectly set.")

    def test_setCourseName_valid_numbers_and_letters(self):
        self.assertTrue(self.course.setCourseName("CS101"), "Valid course name with numbers and letters failed to be set.")

    def test_setCourseName_invalid_unicode(self):
        self.assertFalse(self.course.setCourseName("Étude des systèmes informatiques"),
        "Inalid course name with unicode characters set.")

    def test_setCourseName_valid_spaces_before_after(self):
        self.assertTrue(self.course.setCourseName(" Introduction to Computer Science "),
        "Valid course name with spaces before and after failed to be set.")

    def test_setCourseName_invalid_long_string(self):
        self.assertFalse(self.course.setCourseName("a" * 256), "Course name that is too long was incorrectly set.")

    def test_setCourseName_valid_hyphen(self):
        self.assertTrue(self.course.setCourseName("Intro-to-Computer-Science"),
        "Valid course name with hyphen failed to be set.")

    def test_setCourseName_valid_apostrophe(self):
        self.assertTrue(self.course.setCourseName("Computer Science's Foundation"),
        "Valid course name with apostrophe failed to be set.")

    def test_setCourseName_valid_with_colon(self):
        self.assertTrue(self.course.setCourseName("Introduction: Basic Programming"),
        "Valid course name with colon failed to be set.")

    def test_setCourseName_valid_with_comma(self):
        self.assertTrue(self.course.setCourseName("Computer Science, Introductory Course"),
        "Valid course name with comma failed to be set.")

    def test_setCourseName_invalid_null(self):
        self.assertFalse(self.course.setCourseName(None), "Null course name was incorrectly set.")

class TestSetCourseDescription(unittest.TestCase):
    def setUp(self):
        # Mock the checkDuplicate method for the instantiation, so we don't actually access the DB
        with patch.object(Course, 'checkDuplicate', return_value=False):
            # Create Course object with mocked User
            self.course = Course(
                COURSE_NUMBER=101,
                COURSE_NAME='Introduction to Computer Science',
                COURSE_DESCRIPTION='A beginner\'s course in computer science, covering programming fundamentals.',
                SEMESTER='Fall 2023',
                PREREQUISITES='None',
                DEPARTMENT='Computer Science'
            )
    
    def test_setCourseDescription_valid(self):
        new_description = "An updated course description."
        self.assertTrue(self.course.setCourseDescription(new_description), "Valid course description failed to be set.")

    def test_setCourseDescription_invalid_empty_string(self):
        self.assertFalse(self.course.setCourseDescription(''), "Empty course description string was incorrectly set.")

    def test_setCourseDescription_invalid_whitespace(self):
        self.assertFalse(self.course.setCourseDescription('   '), "Course description with only whitespace was incorrectly set.")

    def test_setCourseDescription_invalid_special_characters(self):
        self.assertFalse(self.course.setCourseDescription('Introduction to CS!@#$%^&*'), "Valid course description with special characters failed to be set.")

    def test_setCourseDescription_valid_spaces_before_after(self):
        new_description = "  An updated course description with spaces.  "
        self.assertTrue(self.course.setCourseDescription(new_description), "Invalid course description with spaces before and after set.")

    def test_setCourseDescription_invalid_unicode(self):
        self.assertFalse(self.course.setCourseDescription('Introduction to CS éàè'), "Valid course description with unicode characters failed to be set.")

    def test_setCourseDescription_valid_with_spaces(self):
        self.assertTrue(self.course.setCourseDescription("Intro to CS and software development"), "Valid course description with spaces failed to be set.")

    def test_setCourseDescription_valid_with_hyphen(self):
        self.assertTrue(self.course.setCourseDescription("Intro to CS - software development"), "Valid course description with hyphen failed to be set.")

    def test_setCourseDescription_valid_with_apostrophe(self):
        self.assertTrue(self.course.setCourseDescription("Intro to CS's concepts"), "Valid course description with apostrophe failed to be set.")

    def test_setCourseDescription_invalid_numbers(self):
        self.assertFalse(self.course.setCourseDescription("1234"), "Course description with numbers was incorrectly set.")

    def test_setCourseDescription_valid_combination(self):
        self.assertTrue(self.course.setCourseDescription("Intro to CS 101"), "Course description with numbers and letters failed to be set.")

    def test_setCourseDescription_valid_mixed_case(self):
        self.assertTrue(self.course.setCourseDescription("iNtro to CoMPuTer sCienCe"), "Valid course description with mixed case failed to be set.")

    def test_setCourseDescription_invalid_only_numbers(self):
        self.assertFalse(self.course.setCourseDescription("1234"), "Course description with only numbers was incorrectly set.")
    
    def test_setCourseDescription_invalid_null(self):
        self.assertFalse(self.course.setCourseDescription(None), "Null course description was incorrectly set.")

class TestSetSemester(unittest.TestCase):
    def setUp(self):
        # Mock the checkDuplicate method for the instantiation, so we don't actually access the DB
        with patch.object(Course, 'checkDuplicate', return_value=False):
            # Create Course object with mocked User
            self.course = Course(
                COURSE_NUMBER=101,
                COURSE_NAME='Introduction to Computer Science',
                COURSE_DESCRIPTION='A beginner\'s course in computer science, covering programming fundamentals.',
                SEMESTER='Fall 2023',
                PREREQUISITES='None',
                DEPARTMENT='Computer Science'
            )

    def test_setSemester_valid(self):
        self.assertTrue(self.course.setSemester('Spring 2023'), "Valid semester failed to be set.")

    def test_setSemester_invalid_empty_string(self):
        self.assertFalse(self.course.setSemester(''), "Empty semester string was incorrectly set.")

    def test_setSemester_invalid_whitespace(self):
        self.assertFalse(self.course.setSemester('   '), "Semester with only whitespace was incorrectly set.")

    def test_setSemester_invalid_special_characters(self):
        self.assertFalse(self.course.setSemester('#$%'), "Semester with special characters was incorrectly set.")

    def test_setSemester_valid_spaces_before_after(self):
        self.assertTrue(self.course.setSemester('  Spring 2023  '), "Semester with spaces before and after was incorrectly set.")

    def test_setSemester_invalid_unicode(self):
        self.assertFalse(self.course.setSemester('Spring 2023é'), "Semester with unicode characters was incorrectly set.")

    def test_setSemester_invalid_long_string(self):
        self.assertFalse(self.course.setSemester('A' * 256), "Semester with too long string was incorrectly set.")

    def test_setSemester_invalid_numbers(self):
        self.assertFalse(self.course.setSemester('123456'), "Semester with numbers was incorrectly set.")
    
    def test_setSemester_valid_mixed_case(self):
        self.assertTrue(self.course.setSemester('SpRiNg 2023'), "Valid semester with mixed case season failed to be set.")

    def test_setSemester_invalid_null(self):
        self.assertFalse(self.course.setSemester(None), "Null semester was incorrectly set.")

class TestSetPrerequisites(unittest.TestCase):
    def setUp(self):
        # Mock the checkDuplicate method for the instantiation, so we don't actually access the DB
        with patch.object(Course, 'checkDuplicate', return_value=False):
            # Create Course object with mocked User
            self.course = Course(
                COURSE_NUMBER=101,
                COURSE_NAME='Introduction to Computer Science',
                COURSE_DESCRIPTION='A beginner\'s course in computer science, covering programming fundamentals.',
                SEMESTER='Fall 2023',
                PREREQUISITES='None',
                DEPARTMENT='Computer Science'
            )
    
    def test_setPrerequisites_valid(self):
        self.assertTrue(self.course.setPrerequisites('CS100'), "Valid prerequisites failed to be set.")

    def test_setPrerequisites_valid_empty_string(self):
        self.assertTrue(self.course.setPrerequisites(''), "Empty prerequisites string failed to be set.")

    def test_setPrerequisites_valid_whitespace(self):
        self.assertTrue(self.course.setPrerequisites('   '), "Prerequisites with only whitespace failed to be set.")

    def test_setPrerequisites_invalid_special_characters(self):
        self.assertFalse(self.course.setPrerequisites('#$%'), "Prerequisites with special characters was incorrectly set.")

    def test_setPrerequisites_valid_spaces_before_after(self):
        self.assertTrue(self.course.setPrerequisites('  CS100  '), "Prerequisites with spaces before and after was incorrectly set.")

    def test_setPrerequisites_invalid_unicode(self):
        self.assertFalse(self.course.setPrerequisites('CS100é'), "Prerequisites with unicode characters was incorrectly set.")

    def test_setPrerequisites_invalid_long_string(self):
        self.assertFalse(self.course.setPrerequisites('A' * 256), "Prerequisites with too long string was incorrectly set.")

    def test_setPrerequisites_valid_multiple_courses(self):
        self.assertTrue(self.course.setPrerequisites('CS100, CS101'), "Valid multiple prerequisites failed to be set.")
    
    def test_setPrerequisites_invalid_numbers(self):
        self.assertFalse(self.course.setPrerequisites('123456'), "Prerequisites with numbers was incorrectly set.")
    
    def test_setSemester_valid_mixed_case(self):
        self.assertTrue(self.course.setPrerequisites('Cs100'), "Valid semester with mixed case prerequisite failed to be set.")
    
    def test_setPrerequisites_valid_null(self):
        self.assertTrue(self.course.setPrerequisites(None), "Null prerequisites failed to be set.")


class TestSetDepartment(unittest.TestCase):
    def setUp(self):
        # Mock the checkDuplicate method for the instantiation, so we don't actually access the DB
        with patch.object(Course, 'checkDuplicate', return_value=False):
            # Create Course object with mocked User
            self.course = Course(
                COURSE_NUMBER=101,
                COURSE_NAME='Introduction to Computer Science',
                COURSE_DESCRIPTION='A beginner\'s course in computer science, covering programming fundamentals.',
                SEMESTER='Fall 2023',
                PREREQUISITES='None',
                DEPARTMENT='Computer Science'
            )
    
    def test_setDepartment_valid(self):
        self.assertTrue(self.course.setDepartment('Mathematics'), "Valid department failed to be set.")

    def test_setDepartment_invalid_empty_string(self):
        self.assertFalse(self.course.setDepartment(''), "Empty department string was incorrectly set.")

    def test_setDepartment_invalid_whitespace(self):
        self.assertFalse(self.course.setDepartment('   '), "Department with only whitespace was incorrectly set.")

    def test_setDepartment_invalid_numbers(self):
        self.assertFalse(self.course.setDepartment('1234'), "Department with numbers was incorrectly set.")

    def test_setDepartment_invalid_special_characters(self):
        self.assertFalse(self.course.setDepartment('#$%'), "Department with special characters was incorrectly set.")

    def test_setDepartment_valid_spaces_before_after(self):
        self.assertTrue(self.course.setDepartment('  Computer Science  '), "Department with spaces before and after failed to be set.")

    def test_setDepartment_invalid_combination(self):
        self.assertFalse(self.course.setDepartment('Math123'), "Department with letters and numbers was incorrectly set.")

    def test_setDepartment_invalid_unicode(self):
        self.assertFalse(self.course.setDepartment('Mathématics'), "Department with unicode characters was incorrectly set.")

    def test_setDepartment_invalid_long_string(self):
        self.assertFalse(self.course.setDepartment('A' * 256), "Department with too long string was incorrectly set.")

    def test_setDepartment_invalid_null(self):
        self.assertFalse(self.course.setDepartment(None), "Null department was incorrectly set.")
