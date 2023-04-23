from django.db import models
from .Course import Course
from .User import User

class CourseAssignment(models.Model):
    COURSE_ASSIGNMENT_ID = models.AutoField(primary_key=True)
    COURSE = models.ForeignKey(Course, on_delete=models.CASCADE)
    TA = models.ForeignKey(User, on_delete=models.CASCADE)
    IS_GRADER = models.BooleanField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        course = kwargs.get('COURSE', None)
        ta = kwargs.get('TA', None)

        if course is None or not isinstance(course, Course):
            raise ValueError("Invalid course")

        if ta is None or not isinstance(ta, User) or ta.ROLE != "TA":
            raise ValueError("Invalid TA")

        if not self.setGrader(kwargs.get('IS_GRADER', None)):
            raise ValueError("Invalid isGrader")

        # Check for duplicate assignment
        if self.checkDuplicate(course, ta):
            raise ValueError("Duplicate assignment")

        # Set COURSE and TA attributes directly
        self.COURSE = course
        self.TA = ta

    def setGrader(self, isGrader):
        if isinstance(isGrader, bool):
            self.IS_GRADER = isGrader
            return True
        else:
            return False

    def checkDuplicate(self, course, ta):
        return CourseAssignment.objects.filter(COURSE=course, TA=ta).exists()
