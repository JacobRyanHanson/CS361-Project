from django.shortcuts import render, redirect
from django.views import View


class DashboardAdmin(View):
    def get(self, request):
        # Check if the user is authenticated using the session
        if not request.session.get('is_authenticated'):
            return redirect("login")
        return render(request, "dashboard-admin.html", {})