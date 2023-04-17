from django.shortcuts import render, redirect
from django.views import View


class User_Creation(View):
    def get(self, request):
        return render(request, "user_creation.html", {})
