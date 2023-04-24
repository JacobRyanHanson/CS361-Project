from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.views import View
from TA_Scheduling_App.models import User


class UserManagement(View):
    def get(self, request):
        # check user is logged in
        if not request.session.get("is_authenticated"):
            return redirect("login")
        # check user is admin - restricted access page
        if request.session.get("user_role") != "ADMIN":
            raise PermissionDenied("You are not permitted to manage other users")

        # get all users from database for display
        users = User.objects.all()
        # users = [ users.first()]

        # annotate logged in user with flag so we do not render 'delete' button
        user_id = request.session.get("user_id")
        for user in users:
            user.deletable = user.USER_ID != user_id

        return render(request, "user-management.html", {'users': users})

