from django.shortcuts import render
from django.views import View


class DashboardAdmin(View):
    def get(self, request):
        return render(request, "dashboard-admin.html", {})
