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
        self.setGrader(kwargs.get('IS_GRADER', None))

    def setGrader(self, isGrader):
        if isinstance(isGrader, bool):
            self.IS_GRADER = isGrader
            return True
        else:
            return False
