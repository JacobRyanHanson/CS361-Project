""" Class-based views
    1. Add an import to views/__init__.py
    2. Add a URL to urlpatterns: path('path/', ViewClass.as_view(), name='view_name'
"""
from django.contrib import admin
from django.urls import path
from TA_Scheduling_App.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Login.as_view(), name='login'),
    path('logout/', Login.as_view(), name='logout'),
    path('home/', Home.as_view(), name="home"),

    path('profile/', AccountSettings.as_view(), name="account_settings"),
    path('dashboard-admin/', DashboardAdmin.as_view(), name="dashboard_admin"),
    path('dashboard-instructor/', DashboardInstructor.as_view(), name="dashboard_instructor"),
    path('dashboard-ta/', DashboardTA.as_view(), name="dashboard_ta"),

    path('course-creation/', CourseCreation.as_view(), name="course_creation"),
    path('section-creation/', SectionManagement.as_view(), name="section_creation"),
    path('user-creation/', UserCreation.as_view(), name="user_creation"),

    path('ta-assignments/', TAAssignments.as_view(), name="ta_assignments"),
    path('user-management/', UserManagement.as_view(), name="user_management"),

    # Missing/future templates
    path('search-contact-information/', Home.as_view(), name='search_contact_information'),
    path('send-notifications/', Home.as_view(), name='send_notifications'),
]
