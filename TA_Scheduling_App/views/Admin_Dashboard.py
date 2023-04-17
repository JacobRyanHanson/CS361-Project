from django.shortcuts import render, redirect
from django.views import View


class Admin_Dashboard(View):
    def get(self, request):
        return render(request, "admin_dashboard.html", {})
