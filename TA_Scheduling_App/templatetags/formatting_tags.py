import datetime
from TA_Scheduling_App.models import User, Course

from django import template

register = template.Library()


@register.filter("html_date")
def html_date(date: datetime.date):
    return date.isoformat()


@register.filter("full_name")
def full_name(user: User):
    if not user:
        return "None"
    return f"{user.FIRST_NAME} {user.LAST_NAME}"


@register.filter("course_name")
def course_name(course: Course):
    return f"{course.DEPARTMENT} {course.COURSE_NUMBER} - {course.COURSE_NAME}"
