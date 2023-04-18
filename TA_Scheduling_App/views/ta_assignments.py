from django.shortcuts import render
from django.views import View


class TAAssignments(View):
    def get(self, request):
        return render(request, "ta-assignments.html", {})
