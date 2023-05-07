from django.core.exceptions import PermissionDenied
from TA_Scheduling_App.models.User import User
from django.shortcuts import render, redirect
from django.views import View
import datetime
from django.db import IntegrityError


class UserCreation(View):
    def get(self, request):
        if not request.session.get("is_authenticated"):
            return redirect("login")
        if request.session.get("user_role") != "ADMIN":
            return redirect("dashboard")

        return render(request, "user-creation.html", {})

    def post(self, request):
        if not request.session.get("is_authenticated"):
            raise PermissionDenied("Not logged in.")
        if request.session.get("user_role") != "ADMIN":
            raise PermissionDenied("You are not permitted to create users.")

        role = request.POST['role']
        first_name = request.POST['firstName']
        last_name = request.POST['lastName']
        email = request.POST['email']
        phone_number = request.POST['phoneNumber']
        address = request.POST['address']

        birth_date = request.POST['birthDate']
        birth_date = datetime.date.fromisoformat(birth_date)

        try:
            user = User(ROLE=role,
                        FIRST_NAME=first_name,
                        LAST_NAME=last_name,
                        EMAIL=email,
                        PASSWORD_HASH="<hashed_password>",
                        PHONE_NUMBER=phone_number,
                        ADDRESS=address,
                        BIRTH_DATE=birth_date)
            user.save()
            status = "Successfully created the user."

        except IntegrityError as e:
            status = "Users with duplicate emails are not allowed."
        except Exception as e:
            status = e

        return render(request, "user-creation.html", {'status': status})
