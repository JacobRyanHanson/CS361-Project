from django.core.exceptions import PermissionDenied
from TA_Scheduling_App.models.Course import Course
from TA_Scheduling_App.models.User import User
from django.shortcuts import render, redirect
from django.views import View


class CourseCreation(View):
    def get(self, request):
        if not request.session.get("is_authenticated"):
            return redirect("login")
        if request.session.get("user_role") != "ADMIN":
            return redirect("dashboard")
        return render(request, "course-creation.html", {})

    def post(self, request):
        if not request.session.get("is_authenticated"):
            raise PermissionDenied("Not logged in.")
        if request.session.get("user_role") != "ADMIN":
            raise PermissionDenied("You are not permitted to create courses.")

        course_number = request.POST['courseNumber']
        instructor_id = request.POST['instructorID']
        course_name = request.POST['courseName']
        course_description = request.POST['courseDescription']
        semester = request.POST['semester']
        prerequisites = request.POST['prerequisites']
        department = request.POST['department']

        try:
            instructor = User.objects.get(USER_ID=instructor_id, ROLE="INSTRUCTOR")

            course = Course(COURSE_NUMBER=course_number,
                            INSTRUCTOR=instructor,
                            COURSE_NAME=course_name,
                            COURSE_DESCRIPTION=course_description,
                            SEMESTER=semester,
                            PREREQUISITES=prerequisites,
                            DEPARTMENT=department)
            course.save()
            status = "Successfully created the course."
        except User.DoesNotExist:
            status = f'The instructor with id {instructor_id} does not exist.'
        except Exception as e:
            status = e

        return render(request, "course-creation.html", {'status': status})
