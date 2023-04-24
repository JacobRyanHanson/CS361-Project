from django.shortcuts import render, redirect
from django.views import View
from TA_Scheduling_App.models.Section import Section


class SectionManagement(View):
    def get(self, request):
        # Check if the user is authenticated using the session
        if not request.session.get('is_authenticated'):
            return redirect("login")
        return render(request, "section-management.html", {})

    def post(self, request):
        COURSE = request.POST['course-associated']  # Update the section's course ID
        SECTION_NUMBER = request.POST['section-number']  # Update the section's section number
        BUILDING = request.POST['building']  # Update the section's building
        ROOM_NUMBER = request.POST['room-number']  # Update the section's room number
        SECTION_START = request.POST['start-time']  # Update the section's start time
        SECTION_END = request.POST['end-time']  # Update the section's end time
        try:
            section = Section(0, SECTION_NUMBER, COURSE,
                              BUILDING, ROOM_NUMBER, SECTION_START, SECTION_END)  # create section object with
                                                                                  # temp section id of 0
        except ValueError as e:
            context = {'status': str(e)}
            return render(request, "section-management.html", context)

        section.save()  # Save the updated section object to the database
        return render(request, "section-management.html", {'status': 'Success!'})
