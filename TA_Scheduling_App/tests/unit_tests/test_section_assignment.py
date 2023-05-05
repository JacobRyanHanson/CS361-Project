import os
import django
import unittest
from unittest.mock import MagicMock, patch

# Set up the Django settings module for testing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TA_Scheduling_Project.settings')
django.setup()

from TA_Scheduling_App.models import Section, Course, User, CourseAssignment, SectionAssignment


class TestSectionAssignmentInit(unittest.TestCase):
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

        # Mock CourseAssignment object
        self.course_assignment = MagicMock(spec=CourseAssignment)
        self.course_assignment.pk = 1
        self.course_assignment.COURSE = self.course
        self.course_assignment.USER = self.ta
        self.course_assignment._state = MagicMock()
        self.course_assignment._state.db = 'default'

        # Mock Section objects
        self.section_lab = MagicMock(spec=Section)
        self.section_lab.pk = 1
        self.section_lab.SECTION_TYPE = "LAB"
        self.section_lab.COURSE = self.course
        self.section_lab._state = MagicMock()
        self.section_lab._state.db = 'default'

        self.section_lecture = MagicMock(spec=Section)
        self.section_lecture.pk = 2
        self.section_lecture.SECTION_TYPE = "LECTURE"
        self.section_lecture.COURSE = self.course
        self.section_lecture._state = MagicMock()
        self.section_lecture._state.db = 'default'

        # Mock another Course object
        self.other_course = MagicMock(spec=Course)
        self.other_course.pk = 2
        self.other_course._state = MagicMock()
        self.other_course._state.db = 'default'

        # Mock User object for another TA
        self.other_ta = MagicMock(spec=User)
        self.other_ta.pk = 2
        self.other_ta._state = MagicMock()
        self.other_ta._state.db = 'default'

        # Mock CourseAssignment object for the other TA
        self.other_course_assignment = MagicMock(spec=CourseAssignment)
        self.other_course_assignment.pk = 2
        self.other_course_assignment.COURSE = self.other_course
        self.other_course_assignment.USER = self.other_ta
        self.other_course_assignment._state = MagicMock()
        self.other_course_assignment._state.db = 'default'

        # Mock CourseAssignment object for instructor
        self.instructor_course_assignment = MagicMock(spec=CourseAssignment)
        self.instructor_course_assignment.pk = 3
        self.instructor_course_assignment.COURSE = self.course
        self.instructor_course_assignment.USER = self.instructor
        self.instructor_course_assignment._state = MagicMock()
        self.instructor_course_assignment._state.db = 'default'

    def test_init_valid_input(self):
        try:
            # Mock the checkDuplicate method for the instantiation, so we don't actually access the DB
            with patch.object(SectionAssignment, 'checkDuplicate', return_value=False):
                SectionAssignment(COURSE_ASSIGNMENT=self.instructor_course_assignment, SECTION=self.section_lecture)
                SectionAssignment(COURSE_ASSIGNMENT=self.course_assignment, SECTION=self.section_lab)
        except ValueError:
            self.fail("SectionAssignment init failed with valid input values.")

    def test_init_invalid_course_assignment(self):
        with self.assertRaises(ValueError,  msg="SectionAssignment init did not raise ValueError for invalid COURSE_ASSIGNMENT"):
            # Mock the checkDuplicate method for the instantiation, so we don't actually access the DB
            with patch.object(SectionAssignment, 'checkDuplicate', return_value=False):
                SectionAssignment(COURSE_ASSIGNMENT=None, SECTION=self.section_lab)

    def test_init_invalid_section(self):
        with self.assertRaises(ValueError, msg="SectionAssignment init did not raise ValueError for invalid SECTION"):
            # Mock the checkDuplicate method for the instantiation, so we don't actually access the DB
            with patch.object(SectionAssignment, 'checkDuplicate', return_value=False):
                SectionAssignment(COURSE_ASSIGNMENT=self.course_assignment, SECTION=None)

    def test_init_invalid_assignment_instructor_to_lab(self):
        with self.assertRaises(ValueError, msg="SectionAssignment init did not raise ValueError for assigning an instructor to a lab section"):
            # Mock the checkDuplicate method for the instantiation, so we don't actually access the DB
            with patch.object(SectionAssignment, 'checkDuplicate', return_value=False):
                SectionAssignment(COURSE_ASSIGNMENT=self.instructor_course_assignment, SECTION=self.section_lab)

    def test_init_invalid_assignment_ta_to_lecture(self):
        with self.assertRaises(ValueError, msg="SectionAssignment init did not raise ValueError for assigning a TA to a lecture section"):
            # Mock the checkDuplicate method for the instantiation, so we don't actually access the DB
            with patch.object(SectionAssignment, 'checkDuplicate', return_value=False):
                SectionAssignment(COURSE_ASSIGNMENT=self.course_assignment, SECTION=self.section_lecture)

    def test_init_course_assignment_section_mismatch_1(self):
        with self.assertRaises(ValueError, msg="SectionAssignment init did not raise ValueError for mismatched COURSE_ASSIGNMENT and SECTION"):
            # Mock the checkDuplicate method for the instantiation, so we don't actually access the DB
            with patch.object(SectionAssignment, 'checkDuplicate', return_value=False):
                SectionAssignment(COURSE_ASSIGNMENT=self.other_course_assignment, SECTION=self.section_lab)

    def test_init_course_assignment_section_mismatch_2(self):
        # Mock Section object for the different course
        different_section = MagicMock(spec=Section)
        different_section.pk = 2
        different_section.SECTION_TYPE = "LAB"
        different_section.COURSE = self.other_course
        different_section._state = MagicMock()
        different_section._state.db = 'default'

        with self.assertRaises(ValueError, msg="SectionAssignment init did not raise ValueError for mismatched COURSE_ASSIGNMENT and SECTION"):
            # Mock the checkDuplicate method for the instantiation, so we don't actually access the DB
            with patch.object(SectionAssignment, 'checkDuplicate', return_value=False):
                SectionAssignment(COURSE_ASSIGNMENT=self.course_assignment, SECTION=different_section)
