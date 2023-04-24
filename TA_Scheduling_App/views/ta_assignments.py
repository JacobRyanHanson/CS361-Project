from django.shortcuts import render, redirect
from django.views import View
from TA_Scheduling_App.models import Course
from django.contrib import messages


class TAAssignments(View):
    def get(self, request):
        # Check if the user is authenticated using the session
        if not request.session.get('is_authenticated'):
            return redirect("login")
        courses = Course.objects.all()

        return render(request, "ta-assignments.html", {'courses': courses})

    def post(self, request):
        # Check if the user is authenticated using the session
        if not request.session.get('is_authenticated'):
            return redirect("login")

        course_id = request.POST.get('course_id')
        if course_id:
            try:
                course = Course.objects.get(COURSE_ID=course_id)
                course.delete()
                status = f'Course with ID {course_id} has been deleted.'
            except Course.DoesNotExist:
                status = f'Course with ID {course_id} does not exist.'
        else:
            status = 'Course ID is missing.'

        courses = Course.objects.all()
        return render(request, "ta-assignments.html", {'courses': courses, 'status': status})