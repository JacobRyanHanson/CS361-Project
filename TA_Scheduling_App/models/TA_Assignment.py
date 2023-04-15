from django.db import models
from .Course import Course
from .Section import Section
from .User import User

class TAAssignment(models.Model):
    TA_ASSIGNMENT_ID = models.AutoField(primary_key=True)
    COURSE = models.ForeignKey(Course, on_delete=models.CASCADE)
    SECTION = models.OneToOneField(Section, on_delete=models.SET_NULL, null=True)
    TA = models.ForeignKey(User, on_delete=models.CASCADE)
    IS_GRADER = models.BooleanField()
