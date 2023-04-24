from django.shortcuts import render, redirect
from django.views import View
from TA_Scheduling_App.models import Course, User, CourseAssignment

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
        instructor_email = request.POST.get('course_instructor')
        course_ta_email = request.POST.get('course_ta_email')
        course_ta_select = request.POST.get('course_ta_select') == 'true'

        # if course_id:
        #     try:
        #         course = Course.objects.get(COURSE_ID=course_id)
        #         course.delete()
        #         status = f'Course with ID {course_id} has been deleted.'
        #     except Course.DoesNotExist:
        #         status = f'Course with ID {course_id} does not exist.'
        # elif instructor_email:
        #     try:
        #         course = Course.objects.get(INSTRUCTOR__EMAIL=instructor_email)

        status = ''

        if instructor_email:
            try:
                instructor = User.objects.get(EMAIL=instructor_email, ROLE="INSTRUCTOR")
                course = Course.objects.get(COURSE_ID=course_id)

                course.setInstructor(instructor)
                course.save()

                status = f'Instructor for course with ID {course_id} has been updated to {instructor_email}.'
            except Course.DoesNotExist:
                status = f'Course with instructor email {instructor_email} does not exist.'
            except User.DoesNotExist:
                status = f'Instructor with instructor email {instructor_email} does not exist.'
        # elif course_ta_email and course_ta_select:
        #     try:
        #         ta = User.objects.get(EMAIL=course_ta_email, ROLE="TA")
        #         course = Course.objects.get(COURSE_ID=course_id)
        #
        #         course_assignment = CourseAssignment(COURSE=None, TA=ta, IS_GRADER=course_ta_select)
        #         course_assignment.save()
        #
        #         status = f'TA {ta.FIRST_NAME} {ta.LAST_NAME} assigned to course {course.COURSE_NAME}.'
        #     except Course.DoesNotExist:
        #         status = f'Course with instructor email {instructor_email} does not exist.'
        #     except User.DoesNotExist:
        #         status = f'Instructor with instructor email {instructor_email} does not exist.'
        #     except

        courses = Course.objects.all()
        return render(request, "ta-assignments.html", {'courses': courses, 'status': status})





        #     try:
        #         course = Course.objects.get(INSTRUCTOR__EMAIL=instructor_email)
        #
        #         if course_id:
        #             course.setInstructor(User.objects.get(EMAIL=instructor_email, ROLE="INSTRUCTOR"))
        #             course.save()
        #             status = f'Instructor for course with ID \'{course_id}\' has been updated to {instructor_email}.'
        #         else:
        #             status = 'Course ID is missing.'
        #
        #     except Course.DoesNotExist:
        #         status = f'Course with instructor email \'{instructor_email}\' does not exist.'
        # else:
        #     status = 'Course ID and instructor email are both missing.'

        # courses = Course.objects.all()
        # return render(request, "ta-assignments.html", {'courses': courses,})
