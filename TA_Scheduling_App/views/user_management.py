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
            return redirect("home")

        user_id = request.session.get("user_id")
        users = User.objects.all()

        for user in users:
            if user.USER_ID == user_id:
                user.safe = True

        return render(request, "user-management.html", {'users': users})

    def post(self, request):
        if not request.session.get("is_authenticated"):
            raise PermissionDenied("Not logged in.")
        # a user deletion has been requested
        # validate access to this operation
        if request.session.get("user_role") != "ADMIN":
            raise PermissionDenied("You are not permitted to delete users")

        user_id = request.session.get("user_id")
        delete_user_id = request.POST.get('delete_user_id')

        try:
            user = User.objects.get(USER_ID=delete_user_id)
            user.delete()

            status = f'User with ID {delete_user_id} has been deleted.'
        except User.DoesNotExist:
            status = f'User with ID {delete_user_id} does not exist.'
        except Exception as e:
            status = e

        users = User.objects.all()

        for user in users:
            if user.USER_ID == user_id:
                user.safe = True

        return render(request, "user-management.html", {'users': users, 'status': status})

