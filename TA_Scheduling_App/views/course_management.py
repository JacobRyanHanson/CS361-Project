from django.core.exceptions import PermissionDenied
from TA_Scheduling_App.models.Course import Course
from TA_Scheduling_App.models.User import User
from django.shortcuts import render, redirect
from django.views import View


class CourseManagement(View):
    def get(self, request):
        if not request.session.get("is_authenticated"):
            return redirect("login")
        if request.session.get("user_role") not in ["ADMIN", "INSTRUCTOR"]:
            raise PermissionDenied("You are not permitted to create courses")

        return render(request, "course-management.html", {})

    def post(self, request):
        COURSE_NUMBER = request.POST['course-number']
        INSTRUCTOR = request.POST['course-instructor']
        COURSE_NAME = request.POST['course-name']
        COURSE_DESCRIPTION = request.POST['course-description']
        SEMESTER = request.POST['semester']
        PREREQUISITES = request.POST['prerequisites']
        DEPARTMENT = request.POST['department']

        try:
            instructor = User.objects.get(pk=INSTRUCTOR)
            course = Course(COURSE_NUMBER=COURSE_NUMBER, INSTRUCTOR=instructor, COURSE_NAME=COURSE_NAME,
                            COURSE_DESCRIPTION=COURSE_DESCRIPTION, SEMESTER=SEMESTER, PREREQUISITES=PREREQUISITES,
                            DEPARTMENT=DEPARTMENT)

        except ValueError as e:
            context = {'status': str(e)}
            return render(request, "course-management.html", context)

        course.save()
        context = {'status': "Successful Course Creation"}
        return render(request, "course-management.html", {context})
