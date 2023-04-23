from django.shortcuts import render
from django.views import View

from TA_Scheduling_App.models import User, Section
from TA_Scheduling_App.null import Null


class Login(View):
    def get(self, request):
        email = "john.doe@example.com"
        user = User.objects.get(EMAIL=email)
        abc = "a"

        return render(request, "login.html", {})
