from django.shortcuts import render
from django.views import View
from dataclasses import dataclass


@dataclass
class User:
    id: int
    type: str
    fname: str
    lname: str
    email: str
    pnumber: str
    address: str
    dob: str


class UserManagement(View):
    def get(self, request):
        sample = User(1, "ADMIN", "Example", "User", "example@example.com", "000-000-0000", "null street", "00-00-0000")
        users = [sample, sample, sample]
        return render(request, "user-management.html", {'users': users})

