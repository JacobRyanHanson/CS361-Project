from django.db import models
from .Course import Course
from .User import User
from abc import ABCMeta
from ..interfaces.i_verification import IVerification
from django.db.models.base import ModelBase

# Used so that the constructor can distinguish between no input Null()
# and 'None' given explicitly as input.
from TA_Scheduling_App.utils.null import Null

# Class to resolve inheritance
class ABCModelMeta(ABCMeta, ModelBase):
    pass


class CourseAssignment(IVerification, models.Model, metaclass=ABCModelMeta):
    COURSE_ASSIGNMENT_ID = models.AutoField(primary_key=True)
    COURSE = models.ForeignKey(Course, on_delete=models.CASCADE)
    TA = models.ForeignKey(User, on_delete=models.CASCADE)
    IS_GRADER = models.BooleanField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        course = kwargs.get('COURSE', Null())

        if course is None or (not isinstance(course, Course) and not Null()):
            raise ValueError("Invalid course")

        if course is not Null():
            self.COURSE = course

        ta = kwargs.get('TA', Null())

        if (ta is None) or (ta is not Null() and ta.ROLE != "TA") or (not isinstance(ta, User) and not Null()):
            raise ValueError("Invalid TA")

        if ta is not Null():
            self.TA = ta

        if not self.setGrader(kwargs.get('IS_GRADER', Null())):
            raise ValueError("Invalid isGrader")

        # Check for duplicate assignment
        if self.checkDuplicate(course, ta):
            raise ValueError("Duplicate assignment failed")

    def setGrader(self, isGrader):
        if isGrader is Null():
            return True

        if isinstance(isGrader, bool):
            self.IS_GRADER = isGrader
            return True
        else:
            return False

    def checkDuplicate(self, course, ta):
        if course is Null() or ta is Null():
            return False
        # Check if the TA is already assigned to the course
        return CourseAssignment.objects.filter(COURSE=course, TA=ta).exists()
