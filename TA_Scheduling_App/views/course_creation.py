from django.core.exceptions import PermissionDenied
from TA_Scheduling_App.models.Course import Course
from TA_Scheduling_App.models.User import User
from TA_Scheduling_App.models.Course_Assignment import CourseAssignment
from django.shortcuts import render, redirect
from django.views import View


class CourseCreation(View):
    def get(self, request):
        if not request.session.get("is_authenticated"):
            return redirect("login")
        if request.session.get("user_role") != "ADMIN":
            return redirect("dashboard")

        instructors = User.objects.filter(ROLE="INSTRUCTOR")

        context = {'instructors': instructors}

        return render(request, "course-creation.html", context)

    def post(self, request):
        if not request.session.get("is_authenticated"):
            raise PermissionDenied("Not logged in.")
        if request.session.get("user_role") != "ADMIN":
            raise PermissionDenied("You are not permitted to create courses.")

        course_number = request.POST['course_number']
        instructor_id = request.POST['instructor_id']
        course_name = request.POST['course_name']
        course_description = request.POST['course_description']
        semester = request.POST['semester']
        prerequisites = request.POST['prerequisites']
        department = request.POST['department']

        try:
            course = Course(COURSE_NUMBER=course_number,
                            COURSE_NAME=course_name,
                            COURSE_DESCRIPTION=course_description,
                            SEMESTER=semester,
                            PREREQUISITES=prerequisites,
                            DEPARTMENT=department)
            course.save()

            instructor = User.objects.get(USER_ID=instructor_id)
            course_assignment = CourseAssignment(COURSE=course, USER=instructor)
            course_assignment.save()

            status = f"Successfully created course {course.COURSE_NAME}."
        except User.DoesNotExist:
            status = f'The instructor does not exist.'
        except Exception as e:
            status = e

        instructors = User.objects.filter(ROLE="INSTRUCTOR")

        context = {'status': status, 'instructors': instructors}

        return render(request, "course-creation.html", context)
