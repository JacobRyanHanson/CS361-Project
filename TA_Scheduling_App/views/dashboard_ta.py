from django.shortcuts import render, redirect
from django.views import View


class DashboardTA(View):
    def get(self, request):
        # verify user is logged in as admin
        if not request.session.get("is_authenticated"):
            return redirect("login")
        if request.session.get("user_role") != "TA":
            # send to home per state machine
            return redirect("home")
        return render(request, "dashboard-ta.html", {})
