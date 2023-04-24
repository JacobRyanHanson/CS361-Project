import datetime
import string
from django.db import models
from .Course import Course
from abc import ABCMeta
from ..interfaces.i_verification import IVerification
from ..interfaces.i_string import IString
from django.db.models.base import ModelBase

# Used so that the constructor can distinguish between no input Null()
# and 'None' given explicitly as input.
from ..null import Null


# Class to resolve inheritance
class ABCModelMeta(ABCMeta, ModelBase):
    pass


class Section(IVerification, IString, models.Model, metaclass=ABCModelMeta):
    SECTION_ID = models.AutoField(primary_key=True)
    SECTION_NUMBER = models.IntegerField()
    COURSE = models.ForeignKey(Course, on_delete=models.CASCADE)
    BUILDING = models.CharField(max_length=255)
    ROOM_NUMBER = models.CharField(max_length=10)
    SECTION_START = models.TimeField()
    SECTION_END = models.TimeField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        course = kwargs.get('COURSE', Null())

        if course is None or (not isinstance(course, Course) and not Null()):
            raise ValueError("Invalid course")

        if course is not Null():
            self.COURSE = course

        if not self.setSectionNumber(kwargs.get('SECTION_NUMBER', Null())):
            raise ValueError("Invalid section number")

        if not self.setBuilding(kwargs.get('BUILDING', Null())):
            raise ValueError("Invalid building")

        if not self.setRoomNumber(kwargs.get('ROOM_NUMBER', Null())):
            raise ValueError("Invalid room number")

        if not self.setSectionStart(kwargs.get('SECTION_START', Null())):
            raise ValueError("Invalid section start time")

        if not self.setSectionEnd(kwargs.get('SECTION_END', Null())):
            raise ValueError("Invalid section end time")

    def setSectionNumber(self, number):
        if number is Null():
            return True

        # Check if the input is an integer
        if not isinstance(number, int):
            return False

        # Check if the input is negative or above the max value
        if number < 0 or number > 9999:
            return False

        # Check for duplicate section number
        if self.checkDuplicate(number):
            return False

        # If all checks pass, set the section number
        self.SECTION_NUMBER = number
        return True

    def setBuilding(self, building):
        if building is Null():
            return True

        building = self.checkString(building)
        if building is False:
            return False

        self.ROOM_NUMBER = building
        return True

    def setRoomNumber(self, roomNumber):
        if roomNumber is Null():
            return True

        roomNumber = self.checkString(roomNumber, True, True, 10)
        if roomNumber is False:
            return False

        self.ROOM_NUMBER = roomNumber
        return True

    def setSectionStart(self, startTime):
        if startTime is Null():
            return True

        if not isinstance(startTime, datetime.time):
            return False

        # Check that start_time is between midnight and 23:59
        if not (datetime.time(0, 0) <= startTime <= datetime.time(23, 59)):
            raise ValueError("Invalid start time")

        self.SECTION_START = startTime
        return True

    def setSectionEnd(self, endTime):
        if endTime is Null():
            return True

        if not isinstance(endTime, datetime.time):
            return False

        if endTime <= self.SECTION_START:
            return False

        if endTime.hour >= 24 or endTime.minute >= 60 or endTime.second >= 60:
            raise ValueError("Invalid end time")

        self.SECTION_END = endTime
        return True

    # Tested in setters
    def checkString(self, value, allowPartialNumeric=True, allowAllNumeric=False, maxLength=255):
        if value is None or not isinstance(value, str) or not value.strip():
            return False

        # Trim whitespace from beginning and end of string
        value = value.strip()

        # Check that string is not too long
        if len(value) > maxLength:
            return False

        # Ensure the string is not completely numeric
        if value.isdigit() and not allowAllNumeric:
            return False

        # Check that string contains only alphanumeric characters, spaces, and certain punctuation marks
        allowed_chars = set(string.ascii_letters + (string.digits if allowPartialNumeric else "") + " -'.:,")
        if not all(c in allowed_chars for c in value):
            return False

        return value

    def checkDuplicate(self, number):
        # Check if the section number is already in use within the same course
        return Section.objects.filter(COURSE=self.COURSE, SECTION_NUMBER=number).exists()
