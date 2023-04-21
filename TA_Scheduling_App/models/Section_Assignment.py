from django.db import models
from .Course_Assignment import CourseAssignment
from .Section import Section


class SectionAssignment(models.Model):
    SECTION_ASSIGNMENT_ID = models.AutoField(primary_key=True)
    COURSE_ASSIGNMENT = models.ForeignKey(CourseAssignment, on_delete=models.CASCADE)
    SECTION = models.ForeignKey(Section, on_delete=models.CASCADE)

