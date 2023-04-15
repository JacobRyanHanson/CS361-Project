from django.db import models
from .Course import Course

class Section(models.Model):
    SECTION_ID = models.AutoField(primary_key=True)
    SECTION_NUMBER = models.IntegerField()
    COURSE = models.ForeignKey(Course, on_delete=models.CASCADE)
    SECTION_CHOICES = (('LAB', 'Lab'), ('LECTURE', 'Lecture'))
    SECTION_TYPE = models.CharField(max_length=10, choices=SECTION_CHOICES)
    BUILDING = models.CharField(max_length=255)
    ROOM_NUMBER = models.CharField(max_length=10)
    SECTION_START = models.TimeField()
    SECTION_END = models.TimeField()
