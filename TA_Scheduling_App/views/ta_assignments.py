from django.shortcuts import render, redirect
from django.views import View
from TA_Scheduling_App.models import Course, User, CourseAssignment, Section, SectionAssignment

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
        section_id = request.POST.get('section_id')
        section_ta_email = request.POST.get('section_ta_email')

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
                status = f'Instructor with email {instructor_email} does not exist.'
            except Exception as e:
                status = e
        elif course_ta_email and isinstance(course_ta_select, bool):
            try:
                ta = User.objects.get(EMAIL=course_ta_email, ROLE="TA")
                course = Course.objects.get(COURSE_ID=course_id)

                course_assignment = CourseAssignment(COURSE=course, TA=ta, IS_GRADER=course_ta_select)
                course_assignment.save()

                status = f'TA {ta.FIRST_NAME} {ta.LAST_NAME} assigned to course {course.COURSE_NAME}.'
            except Course.DoesNotExist:
                status = f'Course with instructor email {instructor_email} does not exist.'
            except User.DoesNotExist:
                status = f'Instructor with email {instructor_email} does not exist.'
            except Exception as e:
                status = e
        elif section_ta_email:
            try:
                ta = User.objects.get(EMAIL=section_ta_email, ROLE="TA")
                course = Course.objects.get(COURSE_ID=course_id)
                section = Section.objects.get(SECTION_ID=section_id)
                course_assignment = CourseAssignment.objects.get(COURSE=course, TA=ta)

                section_assignment = SectionAssignment(COURSE_ASSIGNMENT=course_assignment, SECTION=section)
                section_assignment.save()

                status = f'TA {ta.FIRST_NAME} {ta.LAST_NAME} assigned to section {section.SECTION_NUMBER}.'
            except User.DoesNotExist:
                status = f'TA with email {section_ta_email} does not exist.'
            except Section.DoesNotExist:
                status = f'Section with number {section.SECTION_NUMBER} does not exist.'
            except Exception as e:
                status = e
        elif section_id:
            try:
                section = Section.objects.get(SECTION_ID=section_id)
                section.delete()

                status = f'Section with ID {section_id} has been deleted.'
            except Section.DoesNotExist:
                status = f'Section with ID {section_id} does not exist.'
            except Exception as e:
                status = e
        elif course_id:
            try:
                course = Course.objects.get(COURSE_ID=course_id)
                course.delete()

                status = f'Section with ID {course_id} has been deleted.'
            except Course.DoesNotExist:
                status = f'Section with ID {course_id} does not exist.'
            except Exception as e:
                status = e
        else:
            status = 'An unexpected error occurred.'

        courses = Course.objects.all()
        return render(request, "ta-assignments.html", {'courses': courses, 'status': status})
