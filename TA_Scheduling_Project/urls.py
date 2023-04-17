"""
URL configuration for TA_Scheduling_Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from TA_Scheduling_App.views.Home import Home
from TA_Scheduling_App.views.account_settings import AccountSettings
from TA_Scheduling_App.views.user_management import UserManagement
from TA_Scheduling_App.views.User_Creation import User_Creation
from TA_Scheduling_App.views.Admin_Dashboard import Admin_Dashboard
from TA_Scheduling_App.views.Login import Login
from TA_Scheduling_App.views.Dashboard_TA import Dashboard_TA
from TA_Scheduling_App.views.Dashboard_Instructor import Dashboard_Instructor

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Login.as_view(), name="Login"),
    path('home/', Home.as_view(), name="Home"),
    path('profile/', AccountSettings.as_view(), name="account_settings"),
    path('manage/', UserManagement.as_view(), name="user_management"),
    path('createUser/', User_Creation.as_view()),
    path('dashboardTA/', Dashboard_TA.as_view(), name="Dashboard_TA"),
    path('dashboardInstructor/', Dashboard_Instructor.as_view(), name="Dashboard_Instructor"),
    path('dashboardAdmin/', Admin_Dashboard.as_view()),
]
