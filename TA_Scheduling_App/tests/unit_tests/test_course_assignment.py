import os
import django
import unittest
from unittest.mock import MagicMock

# Set up the Django settings module for testing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TA_Scheduling_Project.settings')
django.setup()

from TA_Scheduling_App.models import Course, User, CourseAssignment


class TestCourseAssignmentInit(unittest.TestCase):
    def setUp(self):
        # Mock Course object
        self.course = MagicMock(spec=Course)
        self.course.pk = 1

        # Mock User object
        self.ta = MagicMock(spec=User)
        self.ta.pk = 1

        # Create CourseAssignment object with mocked Course and User
        self.course_assignment_1 = CourseAssignment(COURSE=self.course, TA=self.ta, IS_GRADER=False)

        # Create CourseAssignment object with mocked Course and User
        self.course_assignment_2 = CourseAssignment(COURSE=self.course, TA=self.ta, IS_GRADER=True)

    def test_init_valid_input(self):
        try:
            CourseAssignment(COURSE=self.course, TA=self.ta, IS_GRADER=False)
            CourseAssignment(COURSE=self.course, TA=self.ta, IS_GRADER=True)
        except ValueError:
            self.fail("CourseAssignment init failed with valid input values.")

    def test_init_invalid_course(self):
        with self.assertRaises(ValueError, msg="CourseAssignment created with invalid course"):
            CourseAssignment(COURSE=None, TA=self.ta, IS_GRADER=False)

    def test_init_invalid_ta(self):
        with self.assertRaises(ValueError, msg="CourseAssignment created with invalid TA"):
            CourseAssignment(COURSE=self.course, TA=None, IS_GRADER=False)

    def test_init_invalid_is_grader(self):
        with self.assertRaises(ValueError, msg="CourseAssignment created with invalid isGrader"):
            CourseAssignment(COURSE=self.course, TA=self.ta, IS_GRADER=None)

    def test_init_duplicate_assignment(self):
        CourseAssignment.objects.create(COURSE=self.course, TA=self.ta, IS_GRADER=False)
        with self.assertRaises(ValueError, msg="CourseAssignment created with duplicate assignment"):
            CourseAssignment(COURSE=self.course, TA=self.ta, IS_GRADER=False)


class TestCourseAssignmentSetGrader(unittest.TestCase):
    def setUp(self):
        # Mock Course object
        self.course = MagicMock(spec=Course)
        self.course.pk = 1

        # Mock User object
        self.ta = MagicMock(spec=User)
        self.ta.pk = 1

        # Create CourseAssignment object with mocked Course and User
        self.course_assignment_1 = CourseAssignment(COURSE=self.course, TA=self.ta, IS_GRADER=False)

        # Create CourseAssignment object with mocked Course and User
        self.course_assignment_2 = CourseAssignment(COURSE=self.course, TA=self.ta, IS_GRADER=True)

    def test_setGrader_valid_true(self):
        result = self.course_assignment_1.setGrader(True)
        self.assertTrue(result, "Failed to set isGrader to True.")
        self.assertEqual(self.course_assignment_1.IS_GRADER, True, "isGrader value not updated to True.")

    def test_setGrader_valid_false(self):
        result = self.course_assignment_2.setGrader(False)
        self.assertTrue(result, "Failed to set isGrader to False.")
        self.assertEqual(self.course_assignment_2.IS_GRADER, False, "isGrader value not updated to False.")

    def test_setGrader_invalid_non_boolean(self):
        result = self.course_assignment_1.setGrader('Not a boolean')
        self.assertFalse(result, "setGrader should return False for non-boolean input.")
        self.assertEqual(self.course_assignment_1.IS_GRADER, False,
                         "isGrader value should not be updated for non-boolean input.")

    def test_setGrader_invalid_null(self):
        result = self.course_assignment_1.setGrader(None)
        self.assertFalse(result, "setGrader should return False for null input.")
        self.assertEqual(self.course_assignment_1.IS_GRADER, False,
                         "isGrader value should not be updated for null input.")

    def test_setGrader_invalid_numeric(self):
        result = self.course_assignment_2.setGrader(1)
        self.assertFalse(result, "setGrader should return False for numeric input.")
        self.assertEqual(self.course_assignment_2.IS_GRADER, False,
                         "isGrader value should not be updated for numeric input.")

    def test_setGrader_invalid_float(self):
        result = self.course_assignment_1.setGrader(1.0)
        self.assertFalse(result, "Failed to reject a float input for isGrader")
        self.assertEqual(self.course_assignment_1.IS_GRADER, False, "isGrader value should not be updated for float input.")

    def test_setGrader_invalid_list(self):
        result = self.course_assignment_1.setGrader([True])
        self.assertFalse(result, "Failed to reject a list input for isGrader")
        self.assertEqual(self.course_assignment_1.IS_GRADER, False, "isGrader value should not be updated for list input.")

    def test_setGrader_invalid_tuple(self):
        result = self.course_assignment_1.setGrader((True,))
        self.assertFalse(result, "Failed to reject a tuple input for isGrader")
        self.assertEqual(self.course_assignment_1.IS_GRADER, False, "isGrader value should not be updated for tuple input.")

    def test_setGrader_invalid_dict(self):
        result = self.course_assignment_1.setGrader({"isGrader": True})
        self.assertFalse(result, "Failed to reject a dictionary input for isGrader")
        self.assertEqual(self.course_assignment_1.IS_GRADER, False,
                     "isGrader value should not be updated for dictionary input.")


