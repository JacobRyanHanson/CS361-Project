from django.db import models
from .Course import Course
from .User import User

class CourseAssignment(models.Model):
    COURSE_ASSIGNMENT_ID = models.AutoField(primary_key=True)
    COURSE = models.ForeignKey(Course, on_delete=models.CASCADE)
    TA = models.ForeignKey(User, on_delete=models.CASCADE)
    IS_GRADER = models.BooleanField()
