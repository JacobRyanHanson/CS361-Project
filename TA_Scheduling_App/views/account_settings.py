import datetime
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.views import View
from TA_Scheduling_App.models import User


class AccountSettings(View):
    def get(self, request):
        # check user is logged in - all users can access their own account settings
        if not request.session.get("is_authenticated"):
            return redirect("login")

        # get known profile information for user
        user = User.objects.get(USER_ID=request.session["user_id"])
        return render(request, "account-settings.html", {'initial': user})

    def post(self, request):
        # user has requested a profile update
        # verify user is logged in
        if not request.session.get("is_authenticated"):
            raise PermissionDenied("Not logged in.")

        user = User.objects.get(USER_ID=request.session["user_id"])

        # validate information provided by user
        first_name = request.POST["firstName"]
        last_name = request.POST["lastName"]
        email = request.POST["email"]
        phone_number = request.POST["phoneNumber"]
        address = request.POST["address"]

        _date_of_birth = request.POST["dateOfBirth"]
        birth_date = datetime.date.fromisoformat(_date_of_birth)

        try:
            User(FIRST_NAME=first_name,
                 LAST_NAME=last_name,
                 EMAIL=email,
                 PHONE_NUMBER=phone_number,
                 ADDRESS=address,
                 BIRTH_DATE=birth_date)
        except Exception as e:
            return render(request, "account-settings.html", {'initial': user, 'status': e})

        # information has been validated, update object
        user.setFirstName(first_name)
        user.setLastName(last_name)
        user.setEmail(email)
        user.setPhoneNumber(phone_number)
        user.setAddress(address)
        user.setBirthDate(birth_date)
        user.save()

        updated = "Your profile changes have been successfully saved."
        return render(request, "account-settings.html", {'initial': user, 'status': updated})
