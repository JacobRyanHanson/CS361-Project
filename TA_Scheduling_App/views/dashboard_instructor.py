from django.shortcuts import render
from django.views import View


class DashboardInstructor(View):
    def get(self, request):
        return render(request, "dashboard-instructor.html", {})
