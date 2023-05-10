from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Prefetch, Subquery, F
from TA_Scheduling_App.models import Course, User, CourseAssignment, Section, SectionAssignment

class TAAssignments(View):
    def context(self, request, status=""):
        user = User.objects.get(USER_ID=request.session["user_id"])

        instructor_prefetch_course = Prefetch(
            'courseassignment_set',
            queryset=CourseAssignment.objects.filter(USER__ROLE='INSTRUCTOR'),
            to_attr='assigned_instructor'
        )

        ta_prefetch_course = Prefetch(
            'courseassignment_set',
            queryset=CourseAssignment.objects.filter(USER__ROLE='TA'),
            to_attr='assigned_tas'
        )

        instructor_prefetch_section = Prefetch(
            'sectionassignment_set',
            queryset=SectionAssignment.objects.filter(COURSE_ASSIGNMENT__USER__ROLE='INSTRUCTOR'),
            to_attr='assigned_instructor'
        )

        ta_prefetch_section = Prefetch(
            'sectionassignment_set',
            queryset=SectionAssignment.objects.filter(COURSE_ASSIGNMENT__USER__ROLE='TA'),
            to_attr='assigned_ta'
        )

        section_prefetch = Prefetch(
            'section_set',
            queryset=Section.objects.prefetch_related(instructor_prefetch_section, ta_prefetch_section).all(),
            to_attr='sections'
        )

        # Append Instructor and TAs assigned to each course.
        courses = Course.objects.prefetch_related(
            instructor_prefetch_course,
            ta_prefetch_course,
            section_prefetch,
        ).all()

        for course in courses:
            # Get instructor from list (should only be one).
            if course.assigned_instructor:
                course.assigned_instructor = course.assigned_instructor[0]
            # Append TAs Not assigned to each course.
            course.unassigned_tas = User.objects.filter(ROLE="TA")\
                .exclude(USER_ID__in=[ta.USER.USER_ID for ta in course.assigned_tas])

            sections = course.sections
            for section in sections:
                # Get instructor from list (should only be one).
                if section.assigned_instructor:
                    section.assigned_instructor = section.assigned_instructor[0].COURSE_ASSIGNMENT
                # Get TA from list (should only be one).
                if section.assigned_ta:
                    section.assigned_ta = section.assigned_ta[0].COURSE_ASSIGNMENT

        instructors = User.objects.filter(ROLE="INSTRUCTOR")

        return {
            'user': user,
            'courses': courses,
            'instructors': instructors,
            'status': status,
        }

    def get(self, request):
        if not request.session.get('is_authenticated'):
            return redirect("login")

        return render(request, "ta-assignments.html", self.context(request))

    def post(self, request):
        if not request.session.get("is_authenticated"):
            raise PermissionDenied("Not logged in.")

        course_id = request.POST.get('course_id')
        section_id = request.POST.get('section_id')

        course_instructor_id = request.POST.get('course_instructor_id')

        course_ta_id = request.POST.get('course_ta_id')
        course_ta_grader_status = request.POST.get('course_ta_grader_status') == 'True'

        section_instructor_id = request.POST.get('section_instructor_id')
        section_ta_id = request.POST.get('section_ta_id')

        status = ""

        if course_instructor_id:
            try:
                course = Course.objects.get(COURSE_ID=course_id)

                old_course_exists = CourseAssignment.objects.filter(COURSE=course, USER__ROLE="INSTRUCTOR").exists()

                if old_course_exists:
                    old_course_assignment = CourseAssignment.objects.get(COURSE=course, USER__ROLE="INSTRUCTOR")

                if course_instructor_id != "None":
                    instructor = User.objects.get(USER_ID=course_instructor_id, ROLE="INSTRUCTOR")
                    course_assignment = CourseAssignment(COURSE=course, USER=instructor)
                    course_assignment.save()

                    status = f'Instructor {instructor.FIRST_NAME} {instructor.LAST_NAME} assigned to course {course.COURSE_NAME}.'

                # Delete old assignment (if it exists) when instructor is None or new assignment is successfully created.
                if old_course_exists:
                    old_course_assignment.delete()
                    # Only update status if it was empty.
                    if status == "":
                        status = f'Instructor was removed from the section.'
            except Course.DoesNotExist:
                status = f'Course does not exist.'
            except User.DoesNotExist:
                status = f'Instructor does not exist.'
            except Exception as e:
                status = e

        elif course_ta_id and isinstance(course_ta_grader_status, bool):
            try:
                ta = User.objects.get(USER_ID=course_ta_id, ROLE="TA")
                course = Course.objects.get(COURSE_ID=course_id)

                course_assignment = CourseAssignment(COURSE=course, USER=ta, IS_GRADER=course_ta_grader_status)
                course_assignment.save()

                status = f'TA {ta.FIRST_NAME} {ta.LAST_NAME} assigned to course {course.COURSE_NAME}.'
            except Course.DoesNotExist:
                status = f'Course does not exist.'
            except User.DoesNotExist:
                status = f'TA does not exist.'
            except Exception as e:
                status = e

        elif section_instructor_id:
            try:
                section = Section.objects.get(SECTION_ID=section_id)

                old_section_exists = SectionAssignment.objects.filter(SECTION=section).exists()

                if old_section_exists:
                    old_section_assignment = SectionAssignment.objects.get(SECTION=section)

                if section_instructor_id != "None":
                    instructor = User.objects.get(USER_ID=section_instructor_id, ROLE="INSTRUCTOR")
                    course = Course.objects.get(COURSE_ID=course_id)
                    course_assignment = CourseAssignment.objects.get(COURSE=course, USER=instructor)

                    section_assignment = SectionAssignment(COURSE_ASSIGNMENT=course_assignment, SECTION=section)
                    section_assignment.save()

                    status = f'Instructor {instructor.FIRST_NAME} {instructor.LAST_NAME} assigned to section.'

                # Delete old assignment (if it exists) when instructor is None or new assignment is successfully created.
                if old_section_exists:
                    old_section_assignment.delete()
                    # Only update status if it was empty.
                    if status == "":
                        status = f'Instructor was removed from the section.'
            except User.DoesNotExist:
                status = f'Instructor does not exist.'
            except Course.DoesNotExist:
                status = f'Course does not exist.'
            except Section.DoesNotExist:
                status = f'Section does not exist.'
            except CourseAssignment.DoesNotExist:
                status = f'The instructor is not assigned to the course.'
            except Exception as e:
                status = e

        elif section_ta_id:
            try:
                section = Section.objects.get(SECTION_ID=section_id)

                old_section_exists = SectionAssignment.objects.filter(SECTION=section).exists()

                if old_section_exists:
                    old_section_assignment = SectionAssignment.objects.get(SECTION=section)

                if section_ta_id != "None":
                    ta = User.objects.get(USER_ID=section_ta_id, ROLE="TA")
                    course = Course.objects.get(COURSE_ID=course_id)
                    course_assignment = CourseAssignment.objects.get(COURSE=course, USER=ta)

                    section_assignment = SectionAssignment(COURSE_ASSIGNMENT=course_assignment, SECTION=section)
                    section_assignment.save()

                    status = f'TA {ta.FIRST_NAME} {ta.LAST_NAME} assigned to section.'

                # Delete old assignment (if it exists) when TA is None or new assignment is successfully created.
                if old_section_exists:
                    old_section_assignment.delete()
                    # Only update status if it was empty.
                    if status == "":
                        status = f'TA was removed from the section.'
            except User.DoesNotExist:
                status = f'TA does not exist.'
            except Course.DoesNotExist:
                status = f'Course does not exist.'
            except Section.DoesNotExist:
                status = f'Section does not exist.'
            except CourseAssignment.DoesNotExist:
                status = f'The TA is not assigned to the course.'
            except Exception as e:
                status = e

        elif section_id:
            try:
                section = Section.objects.get(SECTION_ID=section_id)
                section.delete()

                status = f'Section has been deleted.'
            except Section.DoesNotExist:
                status = f'Section does not exist.'
            except Exception as e:
                status = e

        elif course_id:
            try:
                course = Course.objects.get(COURSE_ID=course_id)
                course.delete()

                status = f'Course {course.COURSE_NAME} has been deleted.'
            except Course.DoesNotExist:
                status = f'Course does not exist.'
            except Exception as e:
                status = e

        else:
            status = 'An unexpected error occurred.'

        return render(request, "ta-assignments.html", self.context(request, status))
