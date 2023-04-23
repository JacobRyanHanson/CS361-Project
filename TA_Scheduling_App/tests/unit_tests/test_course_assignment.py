import os
import django
import unittest
from unittest.mock import MagicMock, patch

# Set up the Django settings module for testing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TA_Scheduling_Project.settings')
django.setup()

from TA_Scheduling_App.models import Course, User, CourseAssignment


class TestCourseAssignmentInit(unittest.TestCase):
    def setUp(self):
        # Mock Course object
        self.course = MagicMock(spec=Course)
        self.course.pk = 1
        self.course._state = MagicMock()
        self.course._state.db = 'default'

        # Mock User objects
        self.ta = MagicMock(spec=User)
        self.ta.pk = 1
        self.ta.ROLE = "TA"
        self.ta._state = MagicMock()
        self.ta._state.db = 'default'

        self.instructor = MagicMock(spec=User)
        self.instructor.pk = 2
        self.instructor.ROLE = "INSTRUCTOR"
        self.instructor._state = MagicMock()
        self.instructor._state.db = 'default'

        self.admin = MagicMock(spec=User)
        self.admin.pk = 3
        self.admin.ROLE = "ADMIN"
        self.admin._state = MagicMock()
        self.admin._state.db = 'default'

    def test_init_valid_input(self):
        try:
            # Mock the checkDuplicate method for the instantiation, so we don't actually access the DB
            with patch.object(CourseAssignment, 'checkDuplicate', return_value=False):
                CourseAssignment(COURSE=self.course, TA=self.ta, IS_GRADER=False)
                CourseAssignment(COURSE=self.course, TA=self.ta, IS_GRADER=True)
        except ValueError:
            self.fail("CourseAssignment init failed with valid input values.")

    def test_init_invalid_course(self):
        with self.assertRaises(ValueError, msg="CourseAssignment created with invalid course"):
            with patch.object(CourseAssignment, 'checkDuplicate', return_value=False):
                CourseAssignment(COURSE=None, TA=self.ta, IS_GRADER=False)

    def test_init_invalid_ta(self):
        with self.assertRaises(ValueError, msg="CourseAssignment created with invalid TA"):
            with patch.object(CourseAssignment, 'checkDuplicate', return_value=False):
                CourseAssignment(COURSE=self.course, TA=None, IS_GRADER=False)

    def test_init_invalid_is_grader(self):
        with self.assertRaises(ValueError, msg="CourseAssignment created with invalid isGrader"):
            with patch.object(CourseAssignment, 'checkDuplicate', return_value=False):
                CourseAssignment(COURSE=self.course, TA=self.ta, IS_GRADER=None)

    def test_wrong_role_instructor(self):
        with self.assertRaises(ValueError, msg="CourseAssignment created with invalid user"):
            with patch.object(CourseAssignment, 'checkDuplicate', return_value=False):
                CourseAssignment(COURSE=self.course, TA=self.instructor, IS_GRADER=False)

    def test_wrong_role_admin(self):
        with self.assertRaises(ValueError, msg="CourseAssignment created with invalid user"):
            with patch.object(CourseAssignment, 'checkDuplicate', return_value=False):
                CourseAssignment(COURSE=self.course, TA=self.admin, IS_GRADER=False)


class TestCourseAssignmentSetGrader(unittest.TestCase):
    def setUp(self):
        # Mock Course object
        self.course = MagicMock(spec=Course)
        self.course.pk = 1
        self.course._state = MagicMock()
        self.course._state.db = 'default'

        # Mock User object
        self.ta = MagicMock(spec=User)
        self.ta.pk = 1
        self.ta.ROLE = "TA"
        self.ta._state = MagicMock()
        self.ta._state.db = 'default'

        # Mock the checkDuplicate method for the instantiation, so we don't actually access the DB
        with patch.object(CourseAssignment, 'checkDuplicate', return_value=False):
            # Create CourseAssignment object with mocked Courses and Users
            self.course_assignment_1 = CourseAssignment(COURSE=self.course, TA=self.ta, IS_GRADER=False)
            self.course_assignment_2 = CourseAssignment(COURSE=self.course, TA=self.ta, IS_GRADER=True)

    def test_setGrader_valid_true(self):
        result = self.course_assignment_1.setGrader(True)
        self.assertTrue(result, "Failed to set isGrader to True.")

    def test_setGrader_valid_false(self):
        result = self.course_assignment_2.setGrader(False)
        self.assertTrue(result, "Failed to set isGrader to False.")

    def test_setGrader_invalid_non_boolean(self):
        result = self.course_assignment_1.setGrader('Not a boolean')
        self.assertFalse(result, "setGrader should return False for non-boolean input.")

    def test_setGrader_invalid_null(self):
        result = self.course_assignment_1.setGrader(None)
        self.assertFalse(result, "setGrader should return False for null input.")

    def test_setGrader_invalid_numeric(self):
        result = self.course_assignment_2.setGrader(1)
        self.assertFalse(result, "setGrader should return False for numeric input.")

    def test_setGrader_invalid_float(self):
        result = self.course_assignment_1.setGrader(1.0)
        self.assertFalse(result, "Failed to reject a float input for isGrader")

    def test_setGrader_invalid_list(self):
        result = self.course_assignment_1.setGrader("True")
        self.assertFalse(result, "Failed to reject string input for isGrader")


