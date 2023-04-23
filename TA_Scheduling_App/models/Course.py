import string
from django.db import models
from .User import User

class Course(models.Model):
    COURSE_ID = models.AutoField(primary_key=True)
    COURSE_NUMBER = models.IntegerField()
    INSTRUCTOR = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    COURSE_NAME = models.CharField(max_length=255)
    COURSE_DESCRIPTION = models.TextField()
    SEMESTER = models.CharField(max_length=255)
    PREREQUISITES = models.CharField(max_length=255)
    DEPARTMENT = models.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.setCourseNumber(kwargs.get('COURSE_NUMBER', None)):
            raise ValueError("Invalid course number")

        if not self.setInstructor(kwargs.get('INSTRUCTOR', None)):
            raise ValueError("Invalid instructor")

        if not self.setCourseName(kwargs.get('COURSE_NAME', None)):
            raise ValueError("Invalid course name")

        if not self.setCourseDescription(kwargs.get('COURSE_DESCRIPTION', None)):
            raise ValueError("Invalid course description")

        if not self.setSemester(kwargs.get('SEMESTER', None)):
            raise ValueError("Invalid semester")

        if not self.setPrerequisites(kwargs.get('PREREQUISITES', None)):
            raise ValueError("Invalid prerequisites")

        if not self.setDepartment(kwargs.get('DEPARTMENT', None)):
            raise ValueError("Invalid department")

    def setCourseNumber(self, number):
        # Check if the input is an integer
        if not isinstance(number, int):
            return False

        # Check if the input is negative or above the max value
        if number < 0 or number > 9999:
            return False

        # Check for duplicate course number
        if self.checkDuplicate(number):
            return False

        # If all checks pass, set the course number
        self.COURSE_NUMBER = number
        return True

    def setInstructor(self, instructor):
        # Allow setting instructor to None
        if instructor is not None and not isinstance(instructor, User):
            return False

        # Check that instructor has the INSTRUCTOR role
        if instructor is not None and instructor.ROLL != "INSTRUCTOR":
            return False

        # Set the instructor for the course
        self.INSTRUCTOR = instructor
        return True

    def setCourseName(self, courseName):
        courseName = self.checkString(courseName)
        if courseName is False:
            return False

        self.COURSE_NAME = courseName
        return True

    def setCourseDescription(self, courseDescription):
        courseDescription = self.checkString(courseDescription)
        if courseDescription is False:
            return False

        self.COURSE_DESCRIPTION = courseDescription
        return True

    def setSemester(self, semester):
        if semester is None or not isinstance(semester, str):
            return False

        # Trim whitespace from beginning and end of semester string
        semester = semester.strip()

        # Check that semester string is not too long
        if len(semester) > 255:
            return False

        # Check that semester string is in the format SEASON YEAR
        semester_parts = semester.split()
        if len(semester_parts) != 2:
            return False
        season, year = semester_parts
        if not (season.isalpha() and year.replace('-', '').isdigit() and len(year) >= 4):
            return False

        # Check that semester string contains only valid characters
        if not all(c.isalpha() or c.isspace() or c.isdigit() or c == '-' for c in semester):
            return False

        self.SEMESTER = semester
        return True

    def setPrerequisites(self, prerequisites):
        prerequisites = self.checkString(prerequisites)
        if prerequisites is False:
            return False

        self.PREREQUISITES = prerequisites
        return True

    def setDepartment(self, department):
        department = self.checkString(department, False)
        if department is False:
            return False

        self.DEPARTMENT = department
        return True

    def checkString(self, value, allow_numeric=True):
        if value is None or not isinstance(value, str) or not value.strip():
            return False

        # Trim whitespace from beginning and end of string
        value = value.strip()

        # Check that string is not too long
        if len(value) > 255:
            return False

        # Ensure the string is not completely numeric
        if value.isdigit():
            return False

        # Check that string contains only alphanumeric characters, spaces, and certain punctuation marks
        allowed_chars = set(string.ascii_letters + (string.digits if allow_numeric else "") + " -'.:,")
        if not all(c in allowed_chars for c in value):
            return False

        return value

    def checkDuplicate(self, number):
        # Check if the course number is already in use within the same department
        return Course.objects.filter(DEPARTMENT=self.DEPARTMENT, COURSE_NUMBER=number).exists()


