from django.db import models
from .Course import Course
from .User import User
from abc import ABCMeta
from ..interfaces.i_verification import IVerification
from django.db.models.base import ModelBase

# Used so that the constructor can distinguish between no input Null()
# and 'None' given explicitly as input.
from TA_Scheduling_App.utils.null import Null


class CourseAssignment(IVerification):
    COURSE_ASSIGNMENT_ID = models.AutoField(primary_key=True)
    COURSE = models.ForeignKey(Course, on_delete=models.CASCADE)
    USER = models.ForeignKey(User, on_delete=models.CASCADE)
    IS_GRADER = models.BooleanField(null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        course = kwargs.get('COURSE', Null())

        if course is None or (not isinstance(course, Course) and not Null()):
            raise ValueError("Invalid course.")

        if course is not Null():
            self.COURSE = course

        user = kwargs.get('USER', Null())

        if (user is None) or (user is not Null() and user.ROLE == "ADMIN") or (not isinstance(user, User) and not Null()):
            raise ValueError("Invalid User.")

        if user is not Null():
            self.USER = user

        if not self.setGrader(kwargs.get('IS_GRADER', Null())):
            raise ValueError("Invalid isGrader.")

        # Check for duplicate assignment
        if self.checkDuplicate(course, user):
            raise ValueError("Duplicate assignment of user to course failed.")

    def setGrader(self, isGrader):
        if isGrader is Null():
            return True

        # Check if the user is an instructor or admin
        if self.USER.ROLE in ['INSTRUCTOR', 'ADMIN']:
            return False

        if isinstance(isGrader, bool):
            self.IS_GRADER = isGrader
            return True
        else:
            return False

    def checkDuplicate(self, course, user):
        if course is Null() or user is Null():
            return False
        # Check if the TA is already assigned to the course
        return CourseAssignment.objects.filter(COURSE=course, USER=user).exists()
