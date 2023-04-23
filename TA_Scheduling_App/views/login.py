from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views import View
from TA_Scheduling_App.models import User


class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("home")
        return render(request, "login.html", {})

    def post(self, request):
        email = request.POST["email"]
        password = request.POST["password"]

        try:
            user = User.objects.get(EMAIL=email)
            is_authenticated = user.PASSWORD_HASH == password
        except User.DoesNotExist:
            user = None
            is_authenticated = False

        if user is not None and is_authenticated:
            request.session['user_id'] = user.USER_ID
            request.session['user_role'] = user.ROLE
            request.session['is_authenticated'] = True
            return redirect("home")
        else:
            context = {'status': "Invalid email or password."}
            return render(request, "login.html", context)
