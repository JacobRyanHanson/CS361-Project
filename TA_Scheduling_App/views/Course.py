from django.shortcuts import render, redirect
from django.views import View


class Course(View):
    def get(self, request):
        return render(request, "sectionManagement.html", {})  # used to debug section and course
