from django.db import models
from .Course_Assignment import CourseAssignment
from .Section import Section

# Used so that the constructor can distinguish between no input Null()
# and 'None' given explicitly as input.
from TA_Scheduling_App.utils.null import Null

class SectionAssignment(models.Model):
    SECTION_ASSIGNMENT_ID = models.AutoField(primary_key=True)
    COURSE_ASSIGNMENT = models.ForeignKey(CourseAssignment, on_delete=models.CASCADE)
    SECTION = models.ForeignKey(Section, on_delete=models.CASCADE)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        courseAssignment = kwargs.get('COURSE_ASSIGNMENT', Null())

        if courseAssignment is None or (not isinstance(courseAssignment, str) and not Null()):
            raise ValueError("Invalid course assignment")

        if courseAssignment is not Null():
            self.COURSE_ASSIGNMENT = courseAssignment

        section = kwargs.get('SECTION', Null())

        if section is None or (not isinstance(section, str) and not Null()):
            raise ValueError("Invalid course assignment")

        if section is not Null():
            self.SECTION = section

        if section is not Null() and courseAssignment is not Null() and section.COURSE != courseAssignment.COURSE:
            raise ValueError("Section is not for the same course as the course assignment")

        # Check for duplicate assignment
        if self.checkDuplicate(courseAssignment, section):
            raise ValueError("Duplicate assignment failed")

    def checkDuplicate(self, courseAssignment, section):
        if courseAssignment is Null() or section is Null():
            return False
        # Check if the TA is already assigned to the section
        return SectionAssignment.objects.filter(COURSE_ASSIGNMENT=courseAssignment, SECTION=section).exists()






