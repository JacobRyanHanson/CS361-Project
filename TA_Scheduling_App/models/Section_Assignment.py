from django.db import models
from .Course_Assignment import CourseAssignment
from .Section import Section


class SectionAssignment(models.Model):
    SECTION_ASSIGNMENT_ID = models.AutoField(primary_key=True)
    COURSE_ASSIGNMENT = models.ForeignKey(CourseAssignment, on_delete=models.CASCADE)
    SECTION = models.ForeignKey(Section, on_delete=models.CASCADE)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        course_assignment = kwargs.get('COURSE_ASSIGNMENT', None)
        section = kwargs.get('SECTION', None)

        if course_assignment is None or not isinstance(course_assignment, CourseAssignment):
            raise ValueError("Invalid course assignment")

        if section is None or not isinstance(section, Section):
            raise ValueError("Invalid section")

        if section.COURSE != course_assignment.COURSE:
            raise ValueError("Section is not for the same course as the course assignment")

        self.COURSE_ASSIGNMENT = course_assignment
        self.SECTION = section

