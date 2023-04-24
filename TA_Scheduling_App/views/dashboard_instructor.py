from django.shortcuts import render, redirect
from django.views import View


class DashboardInstructor(View):
    def get(self, request):
        if not request.session.get("is_authenticated"):
            return redirect("login")
        if request.session.get("user_role") != "INSTRUCTOR":
            return redirect("home")
        return render(request, "dashboard-instructor.html", {})
