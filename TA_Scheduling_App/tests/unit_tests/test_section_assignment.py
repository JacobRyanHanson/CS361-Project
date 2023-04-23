import os
import django
import unittest
from unittest.mock import MagicMock

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

        # Mock User object
        self.ta = MagicMock(spec=User)
        self.ta.pk = 1
        self.ta._state = MagicMock()
        self.ta._state.db = 'default'

        # Mock CourseAssignment object
        self.course_assignment = MagicMock(spec=CourseAssignment)
        self.course_assignment.pk = 1
        self.course_assignment.COURSE = self.course
        self.course_assignment.TA = self.ta
        self.course_assignment._state = MagicMock()
        self.course_assignment._state.db = 'default'

        # Mock Section object
        self.section = MagicMock(spec=Section)
        self.section.pk = 1
        self.section.COURSE = self.course
        self.section._state = MagicMock()
        self.section._state.db = 'default'

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
        self.other_course_assignment.TA = self.other_ta
        self.other_course_assignment._state = MagicMock()
        self.other_course_assignment._state.db = 'default'

    def test_init_valid_input(self):
        try:
            SectionAssignment(COURSE_ASSIGNMENT=self.course_assignment, SECTION=self.section)
        except ValueError:
            self.fail("SectionAssignment init failed with valid input values.")

    def test_init_invalid_course_assignment(self):
        with self.assertRaises(ValueError,
                               msg="SectionAssignment init did not raise ValueError for invalid COURSE_ASSIGNMENT"):
            SectionAssignment(COURSE_ASSIGNMENT=None, SECTION=self.section.pk)

    def test_init_invalid_section(self):
        with self.assertRaises(ValueError,
                               msg="SectionAssignment init did not raise ValueError for invalid SECTION"):
            SectionAssignment(COURSE_ASSIGNMENT=self.course_assignment.pk, SECTION=None)

    def test_init_course_assignment_section_mismatch_1(self):
        with self.assertRaises(ValueError,
                               msg="SectionAssignment init did not raise ValueError for mismatched COURSE_ASSIGNMENT and SECTION"):
            SectionAssignment(COURSE_ASSIGNMENT=self.other_course_assignment, SECTION=self.section)

    def test_init_course_assignment_section_mismatch_2(self):
        # Mock Section object for the different course
        different_section = MagicMock(spec=Section)
        different_section.pk = 2
        different_section.COURSE = self.other_course
        different_section._state = MagicMock()
        different_section._state.db = 'default'

        with self.assertRaises(ValueError,
                               msg="SectionAssignment init did not raise ValueError for mismatched COURSE_ASSIGNMENT and SECTION"):
            SectionAssignment(COURSE_ASSIGNMENT=self.course_assignment, SECTION=different_section)
