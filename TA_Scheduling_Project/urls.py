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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home.as_view()),
    # Temporarily using Home instead of their own template.
    path('account-settings/', Home.as_view(), name='account_settings'),
    path('search-contact-information/', Home.as_view(), name='search_contact_information'),
    path('send-notifications/', Home.as_view(), name='send_notifications'),
    path('ta-dashboard/', Home.as_view(), name='ta_dashboard'),
    path('instructor-dashboard/', Home.as_view(), name='instructor_dashboard'),
    path('admin-dashboard/', Home.as_view(), name='admin_dashboard'),
    path('ta-assignments/', Home.as_view(), name='ta_assignments'),
    path('user-creation/', Home.as_view(), name='user_creation'),
    path('section-creation/', Home.as_view(), name='section_creation'),
    path('course-creation/', Home.as_view(), name='course_creation'),
    path('user-management/', Home.as_view(), name='user_management'),
]
