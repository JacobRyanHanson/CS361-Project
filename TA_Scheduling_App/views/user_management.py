from django.core.exceptions import PermissionDenied, BadRequest
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
            return redirect("dashboard")

        user_id = request.session.get("user_id")
        users = User.objects.all()

        for user in users:
            if user.USER_ID == user_id:
                user.safe = True

        return render(request, "user-management.html", {'users': users})

    def post(self, request):
        if not request.session.get("is_authenticated"):
            raise PermissionDenied("Not logged in.")
        if request.session.get("user_role") != "ADMIN":
            raise PermissionDenied("You are not permitted to delete users.")

        user_id = request.session.get("user_id")
        delete_user_id = request.POST.get('delete_user_id')

        status = ""

        try:
            user = User.objects.get(USER_ID=delete_user_id)
            user.delete()

            status = f'User {user.FIRST_NAME} {user.LAST_NAME} has been deleted.'
        except User.DoesNotExist:
            status = f'User does not exist.'
        except Exception as e:
            status = e

        users = User.objects.all()

        for user in users:
            if user.USER_ID == user_id:
                user.safe = True

        return render(request, "user-management.html", {'users': users, 'status': status})

