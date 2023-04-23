from django.shortcuts import render, redirect
from django.views import View
from TA_Scheduling_App.models import User


class AccountSettings(View):
    def get(self, request):
        # check user is logged in
        if not request.session.get("is_authenticated"):
            return redirect("login")

        # get known profile information for user
        active_user = User.objects.get(USER_ID=request.session["user_id"])
        initial_date = active_user.BIRTH_DATE.isoformat()
        return render(request, "profile.html", {'initial': active_user, 'initial_date': initial_date})
