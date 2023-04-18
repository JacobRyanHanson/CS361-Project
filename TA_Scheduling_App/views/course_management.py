from django.shortcuts import render
from django.views import View


class CourseManagement(View):
    def get(self, request):
        return render(request, "course-management.html", {})

