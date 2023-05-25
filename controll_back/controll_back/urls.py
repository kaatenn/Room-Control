"""
URL configuration for controll_back project.

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
import administrator.views
import login.views
import student.views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('token', login.views.get_csrf_token),
    path('login', login.views.login),
    path('student_room_info', student.views.get_room_info),
    path('student_room_detail', student.views.get_room_detail),
    path('order_computer', student.views.order_computer),
    path('get_user_info', student.views.get_user_info),
    path('student_update_info', student.views.update_info),
    path('shutdown', student.views.shutdown),
    path('administrator_info', administrator.views.get_administrator_info),
    path('administrator_update_info', administrator.views.update_info),
    path('add_computer', administrator.views.add_computer),
    path('delete_computer', administrator.views.delete_computer)
]
