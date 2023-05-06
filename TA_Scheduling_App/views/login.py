from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views import View
from TA_Scheduling_App.models import User


class Login(View):
    def __init__(self, logout=False, **kwargs):
        self.logout = logout
        super().__init__(**kwargs)

    def get(self, request):
        action = request.GET.get('action')

        if request.session.get('is_authenticated'):
            if action == 'logout':
                # Clear the session and log the user out
                request.session.flush()
                return redirect("login")
            else:
                return redirect("dashboard")

        return render(request, "login.html", {'hide_navbar': True})

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
            return redirect("dashboard")
        else:
            return render(request, "login.html", {'status': "Invalid email or password.", 'hide_navbar': True})
