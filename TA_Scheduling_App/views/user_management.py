from django.core.exceptions import PermissionDenied, BadRequest
from django.shortcuts import render, redirect
from django.views import View
from TA_Scheduling_App.models import User


class UserManagement(View):
    def get_users(self, request):
        users = User.objects.all()
        # annotate logged in user with flag so we do not render 'delete' button
        user_id = request.session.get("user_id")
        for user in users:
            user.deletable = user.USER_ID != user_id
        return users

    def get(self, request):
        # check user is logged in
        if not request.session.get("is_authenticated"):
            return redirect("login")
        # check user is admin - restricted access page
        if request.session.get("user_role") != "ADMIN":
            raise PermissionDenied("You are not permitted to manage other users")

        # get all users from database for display
        users = self.get_users(request)
        return render(request, "user-management.html", {'users': users})

    def post(self, request):
        # a user deletion has been requested
        # validate access to this operation
        if request.session.get("user_role") != "ADMIN":
            raise PermissionDenied("You are not permitted to delete users")

        try:
            # get relevant user from database
            target = User.objects.get(USER_ID=request.POST["deleteUserId"])
            deleted = f"User {target.USER_ID}: {target.EMAIL} has been deleted."
            target.delete()

            users = self.get_users(request)
            return render(request, "user-management.html", {'users': users, 'status': deleted})
        except Exception as e:
            print(f"Bad Request to POST user-management: {repr(e)}")
            raise BadRequest()

