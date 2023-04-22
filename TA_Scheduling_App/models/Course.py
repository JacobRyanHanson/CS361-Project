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

    def setCourseNumber(self, number):
        # Check if the input is an integer
        if not isinstance(number, int):
            return False

        # Check if the input is negative or above the max value
        if number < 0 or number > 9999:
            return False

        # Check if the course number is already in use within the same department
        course_exists = Course.objects.filter(DEPARTMENT=self.DEPARTMENT, COURSE_NUMBER=number).exists()
        if course_exists:
            return False

        # If all checks pass, set the course number and save the object
        self.COURSE_NUMBER = number
        self.save()
        return True
