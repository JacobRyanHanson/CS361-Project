from abc import ABCMeta
from ..interfaces.i_verification import IVerification
from django.db import models
from django.db.models.base import ModelBase
from .Course_Assignment import CourseAssignment
from .Section import Section

# Used so that the constructor can distinguish between no input Null()
# and 'None' given explicitly as input.
from TA_Scheduling_App.utils.null import Null


class SectionAssignment(IVerification):
    SECTION_ASSIGNMENT_ID = models.AutoField(primary_key=True)
    COURSE_ASSIGNMENT = models.ForeignKey(CourseAssignment, on_delete=models.CASCADE)
    SECTION = models.ForeignKey(Section, on_delete=models.CASCADE)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        courseAssignment = kwargs.get('COURSE_ASSIGNMENT', Null())

        if courseAssignment is None or (not isinstance(courseAssignment, CourseAssignment) and not Null()):
            raise ValueError("Invalid course assignment")

        if courseAssignment is not Null():
            self.COURSE_ASSIGNMENT = courseAssignment

        section = kwargs.get('SECTION', Null())

        if section is None or (not isinstance(section, Section) and not Null()):
            raise ValueError("Invalid course assignment")

        if section is not Null():
            self.SECTION = section

        if section is not Null() and courseAssignment is not Null() and section.COURSE != courseAssignment.COURSE:
            raise ValueError("Section is not for the same course as the course assignment")

        # Check if instructor is assigned to a lab section
        if section.SECTION_TYPE == 'LAB' and courseAssignment.USER.ROLE == 'INSTRUCTOR':
            raise ValueError("Instructors cannot be assigned to lab sections")

        # Check if ta is assigned to a lecture section
        if section.SECTION_TYPE == 'LECTURE' and courseAssignment.USER.ROLE == 'TA':
            raise ValueError("TAs cannot be assigned to lecture sections")

        # Check for duplicate assignment
        if self.checkDuplicate(courseAssignment, section):
            raise ValueError("Duplicate assignment of TA to section failed")

    def checkDuplicate(self, courseAssignment, section):
        if courseAssignment is Null() or section is Null():
            return False
        # Check if the TA is already assigned to the section
        return SectionAssignment.objects.filter(COURSE_ASSIGNMENT=courseAssignment, SECTION=section).exists()
