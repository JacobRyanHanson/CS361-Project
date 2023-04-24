import datetime

from django import template

register = template.Library()

@register.filter("html_date")
def html_date(date: datetime.date):
    return date.isoformat()
