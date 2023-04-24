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
        course_number = request.POST['course-number']
        instructor = request.POST['course-instructor']
        course_name = request.POST['course-name']
        course_description = request.POST['course-description']
        semester = request.POST['semester']
        prerequisites = request.POST['prerequisites']
        department = request.POST['department']

        try:
            course = Course(COURSE_NUMBER=course_number, INSTRUCTOR=User.objects.get(pk=instructor),
                            COURSE_NAME=course_name, COURSE_DESCRIPTION=course_description, SEMESTER=semester,
                            PREREQUISITES=prerequisites, DEPARTMENT=department)

        except ValueError as e:
            context = {'status': str(e)}
            return render(request, "course-management.html", context)

        course.save()
        context = {'status': "Successful Course Creation"}
        return render(request, "course-management.html", context)
