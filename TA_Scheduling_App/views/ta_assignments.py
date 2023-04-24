from django.shortcuts import render, redirect
from django.views import View
from TA_Scheduling_App.models import Course

class TAAssignments(View):
    def get(self, request):
        # Check if the user is authenticated using the session
        if not request.session.get('is_authenticated'):
            return redirect("login")
        courses = Course.objects.all()

        return render(request, "ta-assignments.html", {'courses': courses})