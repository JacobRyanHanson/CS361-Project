import string
from django.db import models
from .User import User
from abc import ABCMeta
from ..interfaces.i_verification import IVerification
from ..interfaces.i_string import IString
from django.db.models.base import ModelBase

# Used so that the constructor can distinguish between no input Null()
# and 'None' given explicitly as input.
from TA_Scheduling_App.utils.null import Null

# Class to resolve inheritance
class ABCModelMeta(ABCMeta, ModelBase):
    pass

class Course(IVerification, IString, models.Model, metaclass=ABCModelMeta):
    COURSE_ID = models.AutoField(primary_key=True)
    COURSE_NUMBER = models.IntegerField()
    INSTRUCTOR = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    COURSE_NAME = models.CharField(max_length=255)
    COURSE_DESCRIPTION = models.TextField()
    SEMESTER = models.CharField(max_length=255)
    PREREQUISITES = models.CharField(max_length=255, null=True)
    DEPARTMENT = models.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        result = self.setCourseNumber(kwargs.get('COURSE_NUMBER', Null()))

        if result == False:
            raise ValueError("Invalid course number")
        elif result == None:
            raise ValueError("Duplicate course number assignment failed")

        if not self.setInstructor(kwargs.get('INSTRUCTOR', Null())):
            raise ValueError("Invalid instructor")

        if not self.setCourseName(kwargs.get('COURSE_NAME', Null())):
            raise ValueError("Invalid course name")

        if not self.setCourseDescription(kwargs.get('COURSE_DESCRIPTION', Null())):
            raise ValueError("Invalid course description")

        if not self.setSemester(kwargs.get('SEMESTER', Null())):
            raise ValueError("Invalid semester")

        if not self.setPrerequisites(kwargs.get('PREREQUISITES', Null())):
            raise ValueError("Invalid prerequisites")

        if not self.setDepartment(kwargs.get('DEPARTMENT', Null())):
            raise ValueError("Invalid department")

    def setCourseNumber(self, number):
        if number is Null():
            return True

        try:
            if isinstance(number, float):
                return False
            int_value = int(number)
        except Exception:
            return False

        # Check if the input is negative or above the max value
        if int_value < 0 or int_value > 9999:
            return False

        # Check for duplicate course number
        if self.checkDuplicate(int_value):
            return None

        # If all checks pass, set the course number
        self.COURSE_NUMBER = int_value
        return True

    def setInstructor(self, instructor):
        if instructor is Null():
            return True

        # Allow setting instructor to None
        if instructor is not None and not isinstance(instructor, User):
            return False

        # Check that instructor has the INSTRUCTOR role
        if instructor is not None and instructor.ROLE != "INSTRUCTOR":
            return False

        # Set the instructor for the course
        self.INSTRUCTOR = instructor
        return True

    def setCourseName(self, courseName):
        if courseName is Null():
            return True

        result = self.checkString(courseName)
        if result is False:
            return False

        self.COURSE_NAME = courseName
        return True

    def setCourseDescription(self, courseDescription):
        if courseDescription is Null():
            return True

        result = self.checkString(courseDescription)
        if result is False:
            return False

        self.COURSE_DESCRIPTION = courseDescription
        return True

    def setSemester(self, semester):
        if semester is Null():
            return True

        if semester is None or not isinstance(semester, str):
            return False

        # Trim whitespace from beginning and end of semester string
        semester = semester.strip()

        # Check that semester string is not empty, not only whitespace, and not only numbers
        if not semester or semester.isspace() or semester.isdigit():
            return False

        # Check that semester string is not too long
        if len(semester) > 255:
            return False

        # Check that semester string contains only valid characters and is ASCII
        if not all((c.isalpha() or c.isspace() or c.isdigit() or c == '-') and c.isascii() for c in semester):
            return False

        self.SEMESTER = semester
        return True

    def setPrerequisites(self, prerequisites):
        if prerequisites is Null():
            return True

        result = self.checkString(prerequisites, True, True)
        if result is False:
            return False

        self.PREREQUISITES = prerequisites
        return True

    def setDepartment(self, department):
        if department is Null():
            return True

        result = self.checkString(department, False)
        if result is False:
            return False

        self.DEPARTMENT = department
        return True

    def checkString(self, value, allowPartialNumeric=True, allowEmpty=False):
        if (value is None or not isinstance(value, str) or not value.strip()) and not allowEmpty:
            return False

        # For empty strings, return True if they are allowed
        if allowEmpty and (value is None or not value.strip()):
            return True

        # Trim whitespace from beginning and end of string
        value = value.strip()

        # Check that string is not too long
        if len(value) > 255:
            return False

        # Ensure the string is not completely numeric
        if value.isdigit():
            return False

        # Check that string contains only alphanumeric characters, spaces, and certain punctuation marks
        allowed_chars = set(string.ascii_letters + (string.digits if allowPartialNumeric else "") + " -'.:,")
        if not all(c in allowed_chars for c in value):
            return False

        return value

    def checkDuplicate(self, number):
        if number is Null():
            return False
        # Check if the course number is already in use within the same department
        return Course.objects.filter(DEPARTMENT=self.DEPARTMENT, COURSE_NUMBER=number).exists()


