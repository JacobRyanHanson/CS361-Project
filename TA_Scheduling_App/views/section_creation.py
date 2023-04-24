from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.views import View
from TA_Scheduling_App.models.Section import Section, Course
from datetime import *

class SectionCreation(View):
    def get(self, request):
        if not request.session.get("is_authenticated"):
            return redirect("login")
        if request.session.get("user_role") != "ADMIN":
            return redirect("home")

        context = {'h_range': range(1, 25),
                   'm_range': range(0, 60)}

        return render(request, "section-creation.html", context)

    def post(self, request):
        if not request.session.get("is_authenticated"):
            raise PermissionDenied("Not logged in.")
        if request.session.get("user_role") != "ADMIN":
            raise PermissionDenied("You are not permitted to create sections.")

        course_id = request.POST['courseID']
        section_number = request.POST['sectionNumber']
        building = request.POST['building']
        room_number = request.POST['roomNumber']
        start_time_h = request.POST['startTimeH']
        start_time_m = request.POST['startTimeM']
        end_time_h = request.POST['endTimeH']
        end_time_m = request.POST['endTimeM']

        try:
            course = Course.objects.get(COURSE_ID=course_id)

            start_time_h = int(start_time_h)
            start_time_m = int(start_time_m)
            start_time = time(start_time_h, start_time_m)

            end_time_h = int(end_time_h)
            end_time_m = int(end_time_m)
            end_time = time(end_time_h, end_time_m)

            section = Section(SECTION_NUMBER=section_number,
                              COURSE=course,
                              BUILDING=building,
                              ROOM_NUMBER=room_number,
                              SECTION_START=start_time,
                              SECTION_END=end_time)
            section.save()
            status = "Successful Section Creation"
        except Course.DoesNotExist:
            status = f'The course with id {course_id} does not exist.'
        except Exception as e:
            status = e

        context = {'h_range': range(1, 25),
                   'm_range': range(0, 60),
                   'status': status}

        return render(request, "section-creation.html", context)
