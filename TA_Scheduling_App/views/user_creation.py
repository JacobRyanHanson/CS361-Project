from django.core.exceptions import PermissionDenied
from TA_Scheduling_App.models.User import User
from django.shortcuts import render, redirect
from django.views import View


class UserCreation(View):
    def get(self, request):
        if not request.session.get("is_authenticated"):
            return redirect("login")
        if request.session.get("user_role") not in ["ADMIN"]:
            raise PermissionDenied("You are not permitted to create users")

        return render(request, "user-creation.html", {})

    def post(self, request):
        role = request.POST['userType']
        first_name = request.POST['firstName']
        last_name = request.POST['lastName']
        email = request.POST['email']
        phone_number = request.POST['phoneNumber']
        address = request.POST['address']
        birth_date = request.POST['dateOfBirth']

        try:
            user = User(ROLE=role, FIRST_NAME=first_name, LAST_NAME=last_name, EMAIL=email,
                        PASSWORD_HASH="<hashed_password>", PHONE_NUMBER=phone_number,
                        ADDRESS=address, BIRTH_DATE=birth_date)

        except ValueError as e:
            context = {'status': str(e)}
            return render(request, "user-creation.html", context)

        user.save()
        context = {'status': "Successful User Creation"}
        return render(request, "user-creation.html", context)
