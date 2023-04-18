from django.shortcuts import render
from django.views import View


class UserCreation(View):
    def get(self, request):
        return render(request, "user-creation.html", {})
