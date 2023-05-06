from django.shortcuts import render, redirect
from django.views import View
from TA_Scheduling_App.models import User


class Dashboard(View):
    def get(self, request):
        if not request.session.get('is_authenticated'):
            return redirect("login")

        user = User.objects.get(USER_ID=request.session["user_id"])
        return render(request, "dashboard.html", {'role': user.ROLE})
