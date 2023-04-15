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