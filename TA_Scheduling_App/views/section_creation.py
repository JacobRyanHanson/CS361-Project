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
            return redirect("dashboard")

        return render(request, "section-creation.html")

    def post(self, request):
        if not request.session.get("is_authenticated"):
            raise PermissionDenied("Not logged in.")
        if request.session.get("user_role") != "ADMIN":
            raise PermissionDenied("You are not permitted to create sections.")

        course_id = request.POST['courseID']
        section_number = request.POST['sectionNumber']
        building = request.POST['building']
        room_number = request.POST['roomNumber']
        start_time = request.POST['startTime']
        end_time = request.POST['endTime']

        try:
            course = Course.objects.get(COURSE_ID=course_id)
            
            start_time = datetime.strptime(start_time, '%H:%M').time()
            end_time = datetime.strptime(end_time, '%H:%M').time()

            section = Section(SECTION_NUMBER=section_number,
                              COURSE=course,
                              BUILDING=building,
                              ROOM_NUMBER=room_number,
                              SECTION_START=start_time,
                              SECTION_END=end_time)
            section.save()
            status = "Successfully created the section."
        except Course.DoesNotExist:
            status = f'The course with id {course_id} does not exist.'
        except Exception as e:
            status = e

        context = {'status': status}

        return render(request, "section-creation.html", context)
