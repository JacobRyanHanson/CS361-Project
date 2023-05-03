from django.shortcuts import render, redirect
from django.views import View


class Home(View):
    def get(self, request):
        if not request.session.get("is_authenticated"):
            return redirect("login")
        if request.session.get("user_role") == "ADMIN":
            return render(request, "dashboard-admin.html", {})
        elif request.session.get("user_role") == "INSTRUCTOR":
            return render(request, "dashboard-instructor.html", {})
        elif request.session.get("user_role") == "TA":
            return render(request, "dashboard-ta.html", {})
