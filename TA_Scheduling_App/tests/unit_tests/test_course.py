from TA_Scheduling_App.models.Course import Course
import unittest

class test_getInfo(unittest.TestCase):
    def setUp(self):
        self.course = Course(courseID=361, courseNumber=3, instructorID=24, courseName="Example Course",
                             courseDescription="Learning",
                             semester="Fall 2023", prerequisites="CS351", department="Computer Science")
    def test_get(self):
        testDict = {'courseID': 361, 'courseNumber': 3, 'instructorID': 24,
                    'courseName': "Example Course", 'courseDescription': "Learning", 'semester': "Fall 2023",
                    'prerequisites': "CS351", 'department': "Computer Science"}
        self.assertEqual(testDict, self.course.getInfo)

class test_setCourseNumber(unittest.TestCase):
    def setUp(self):
        self.course = Course(courseID=361, courseNumber=3, instructorID=24, courseName="Example Course",
                             courseDescription="Learning",
                             semester="Fall 2023", prerequisites="CS351", department="Computer Science")
    def test_setCourseNumber_valid(self):
        self.assertTrue(self.course.setCourseNumber(6))

    def test_setCourseNumber_invalidNegative(self):
        self.assertFalse(self.course.setCourseNumber(-2))

    def test_setCourseNumber_invalidType(self):
        with self.assertRaises(TypeError, msg="Non-Numeric data cannot be passed to setCourseNumber"):
            self.course.setCourseNumber("seven")

    def test_setCourseNumber_invalid_null(self):
        self.assertFalse(self.course.setCourseNumber(None))

class test_setInstructorID(unittest.TestCase):
    def setUp(self):
        self.course = Course(courseID=361, courseNumber=3, instructorID=24, courseName="Example Course",
                             courseDescription="Learning",
                             semester="Fall 2023", prerequisites="CS351", department="Computer Science")
    def test_setInstructorID_valid(self):
        self.assertTrue(self.course.setInstructorID(6))

    def test_setInstructorID_invalidNegative(self):
        self.assertFalse(self.course.setInstructorID(-2))

    def test_setInstructorID_invalidType(self):
        with self.assertRaises(TypeError, msg="Non-Numeric data cannot be passed to setInstructorID"):
            self.course.setInstructorID("seven")

    def test_setInstructorID_invalid_null(self):
        self.assertFalse(self.course.setInstructorID(None))


class test_setCourseName(unittest.TestCase):
    def setUp(self):
        self.course = Course(courseID=361, courseNumber=3, instructorID=24, courseName="Example Course",
                             courseDescription="Learning",
                             semester="Fall 2023", prerequisites="CS351", department="Computer Science")

    def test_setCourseName_valid(self):
        self.assertTrue(self.course.setCourseName("Intro to Computer Science"))

    def test_setCourseName_valid_with_hyphen(self):
        self.assertTrue(self.course.setCourseName("Calculus-Based Physics"))

    def test_setCourseName_valid_with_apostrophe(self):
        self.assertTrue(self.course.setCourseName("Study of Euler's Formula"))

    def test_setCourseName_invalid_empty_string(self):
        self.assertFalse(self.course.setCourseName(""))

    def test_setCourseName_invalid_whitespace(self):
        self.assertFalse(self.course.setCourseName("   "))

    def test_setCourseName_invalid_special_characters(self):
        self.assertFalse(self.course.setCourseName("#$%@"))

    def test_setCourseName_valid_combination(self):
        self.assertFalse(self.course.setCourseName("CS361"))

    def test_setCourseName_valid_unicode(self):
        self.assertTrue(self.course.setCourseName("español"))

    def test_setCourseName_valid_spaces_before_after(self):
        self.assertTrue(self.course.setCourseName("  CS361  "))

    def test_setCourseName_invalid_long_string(self):
        self.assertFalse(self.course.setCourseName("a" * 256))

    def test_setCourseName_valid_one_letter(self):
        self.assertTrue(self.course.setCourseName("C"))

    def test_setCourseName_invalid_null(self):
        self.assertFalse(self.course.setCourseName(None))
class test_setCourseDescription(unittest.TestCase):
    def setUp(self):
        self.course = Course(courseID=361, courseNumber=3, instructorID=24, courseName="Example Course",
                             courseDescription="Learning",
                             semester="Fall 2023", prerequisites="CS351", department="Computer Science")

    def test_setCourseDescription_valid(self):
        self.assertTrue(self.course.setCourseDescription("Learning stuff"))

    def test_setCourseDescription_valid_with_hyphen(self):
        self.assertTrue(self.course.setCourseDescription("Calculus-Based Physics"))

    def test_setCourseDescription_valid_with_apostrophe(self):
        self.assertTrue(self.course.setCourseDescription("Course teaches students the abc's"))

    def test_setCourseDescription_invalid_empty_string(self):
        self.assertFalse(self.course.setCourseDescription(""))

    def test_setCourseDescription_invalid_whitespace(self):
        self.assertFalse(self.course.setCourseDescription("   "))

    def test_setCourseDescription_valid_combination(self):
        self.assertFalse(self.course.setCourseDescription("Learn 3 new programming languages"))

    def test_setCourseName_valid_unicode(self):
        self.assertTrue(self.course.setCourseName("Para estudiantes que hablan español"))

    def test_setCourseName_valid_spaces_before_after(self):
        self.assertTrue(self.course.setCourseName("  Learning Stuff  "))

    def test_setCourseName_invalid_long_string(self):
        self.assertFalse(self.course.setCourseName("a" * 256))

    def test_setCourseName_valid_one_letter(self):
        self.assertTrue(self.course.setCourseName("C"))

    def test_setCourseName_invalid_null(self):
        self.assertFalse(self.course.setCourseName(None))
