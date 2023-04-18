from django.shortcuts import render
from django.views import View


class SectionManagement(View):
    def get(self, request):
        return render(request, "section-management.html", {})

