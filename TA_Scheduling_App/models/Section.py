from django.db import models
from .Course import Course


class Section(models.Model):
    SECTION_ID = models.AutoField(primary_key=True)
    SECTION_NUMBER = models.IntegerField()
    COURSE = models.ForeignKey(Course, on_delete=models.CASCADE)
    BUILDING = models.CharField(max_length=255)
    ROOM_NUMBER = models.CharField(max_length=10)
    SECTION_START = models.TimeField()
    SECTION_END = models.TimeField()
