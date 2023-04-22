from django.db import models
from TA_Scheduling_App.models import Course


class Section(models.Model):
    SECTION_ID = models.AutoField(primary_key=True)
    SECTION_NUMBER = models.IntegerField()
    COURSE = models.ForeignKey(Course, on_delete=models.CASCADE)
    BUILDING = models.CharField(max_length=255)
    ROOM_NUMBER = models.CharField(max_length=10)
    SECTION_START = models.TimeField()
    SECTION_END = models.TimeField()

    def __init__(self, section_num, course, building, room_num, section_start, section_end):
        self.set_section_num(section_num)
        self.COURSE = course
        self.set_building(building)
        self.set_room_number(room_num)
        self.set_section_start(section_start)
        self.set_section_end(section_end)
        self.save()

    def get_section(section_id):
        return Section.objects.get(section_id=section_id)

    def get_section_num(self):
        return self.SECTION_NUMBER

    def set_section_num(self, new_section_num):
        if new_section_num is None:
            raise Exception("Section number is null")
        elif not new_section_num.isdigit():
            raise Exception("Section number not a number")
        elif new_section_num < 0 or new_section_num > 9999:
            raise Exception("Section number too large or small")
        else:
            self.SECTION_NUMBER = new_section_num

    def get_course(self):
        return self.COURSE

    def get_building(self):
        return self.BUILDING

    def set_building(self, new_building):
        if new_building is None:
            raise Exception("new building can't be null")
        else:
            self.BUILDING = new_building

    def get_room_number(self):
        return self.room_number

    def set_room_number(self, new_room_number):
        if new_room_number is None:
            raise Exception("New room number can't be null")
        else:
            self.room_number = new_room_number

    def get_section_start(self):
        return self.SECTION_START

    def set_section_start(self, new_section_start):
        if new_section_start is None:
            raise Exception("Start time not null")
        else:
            self.SECTION_START = new_section_start

    def get_section_end(self):
        return self.SECTION_END

    def set_section_end(self, new_section_end):
        if new_section_end is None:
            raise Exception("Start time not null")
        else:
            self.SECTION_END = new_section_end
