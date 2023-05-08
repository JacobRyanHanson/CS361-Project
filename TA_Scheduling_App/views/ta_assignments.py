from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Prefetch
from TA_Scheduling_App.models import Course, User, CourseAssignment, Section, SectionAssignment

class TAAssignments(View):
    def context(self, request, status=""):
        user = User.objects.get(USER_ID=request.session["user_id"])

        ta_prefetch = Prefetch('courseassignment_set', queryset=CourseAssignment.objects.filter(USER__ROLE='TA'), to_attr='assigned_tas')
        courses = Course.objects.prefetch_related(ta_prefetch).all()
        course_assignments = CourseAssignment.objects.all()
        instructors = User.objects.filter(ROLE="INSTRUCTOR")

        return {
            'role': user.ROLE,
            'courses': courses,
            'status': status,
            'course_assignments' : course_assignments,
            'instructors' : instructors
        }

    def get(self, request):
        if not request.session.get('is_authenticated'):
            return redirect("login")

        return render(request, "ta-assignments.html", self.context(request))

    def post(self, request):
        if not request.session.get("is_authenticated"):
            raise PermissionDenied("Not logged in.")

        course_id = request.POST.get('course_id')
        instructor_id = request.POST.get('course_instructor_id')
        course_ta_email = request.POST.get('course_ta_email')
        course_ta_select = request.POST.get('course_ta_select') == 'true'
        section_id = request.POST.get('section_id')
        section_ta_email = request.POST.get('section_ta_email')

        status = ''

        if instructor_id:
            try:
                instructor = User.objects.get(USER_ID=instructor_id)
                course = Course.objects.get(COURSE_ID=course_id)

                course_assignment = CourseAssignment.objects.filter(COURSE=course)
                for c in course_assignment:
                    if(c.USER.ROLE == 'INSTRUCTOR'):
                        c.delete()

                course_assignment = CourseAssignment(COURSE=course, USER=instructor)
                course_assignment.save()


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
                status = f'Course with number {course.COURSE_NUMBER} does not exist.'
            except User.DoesNotExist:
                status = f'TA with email {course_ta_email} does not exist.'
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
            except Course.DoesNotExist:
                status = f'Course with number {course.COURSE_NUMBER} does not exist.'
            except Section.DoesNotExist:
                status = f'Section with number {section.SECTION_NUMBER} does not exist.'
            except CourseAssignment.DoesNotExist:
                status = f'The TA is not assigned to the course.'
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

                status = f'Course with ID {course_id} has been deleted.'
            except Course.DoesNotExist:
                status = f'Course with ID {course_id} does not exist.'
            except Exception as e:
                status = e
        else:
            status = 'An unexpected error occurred.'

        return render(request, "ta-assignments.html", self.context(request, status))
