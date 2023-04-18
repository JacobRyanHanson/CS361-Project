from django.shortcuts import render
from django.views import View
from dataclasses import dataclass


@dataclass
class User:
    id: int
    type: str
    firstName: str
    lastName: str
    email: str
    phoneNumber: str
    address: str
    dateOfBirth: str


class UserManagement(View):
    def get(self, request):
        sample = User(1, "ADMIN", "Example", "User", "example@example.com", "000-000-0000", "null street", "00-00-0000")
        users = [sample, sample, sample]
        return render(request, "user-management.html", {'users': users})

