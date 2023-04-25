from django.shortcuts import render, redirect
from django.views import View

class Home(View):
    def get(self, request):
        if not request.session.get('is_authenticated'):
            return redirect("login")
        return render(request, "home.html", {})
