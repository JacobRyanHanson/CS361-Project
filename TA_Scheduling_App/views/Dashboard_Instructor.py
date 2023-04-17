from django.shortcuts import render, redirect
from django.views import View


class Dashboard_Instructor(View):
    def get(self, request):
        return render(request, "Dashboard_Instructor.html", {})