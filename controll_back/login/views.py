from django.shortcuts import render
import django.middleware.csrf
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from common.models import *

# Create your views here.

def get_csrf_token(request):
    django.middleware.csrf.get_token(request)
    return HttpResponse('Successfully get csrf token')

def login(request):
    if request.method == 'POST':
        user_info = request.POST
        account = user_info['account']
        password = user_info['password']
        if user_info['type'] == 'administrator':
            user = Administrator.objects.filter(ad_id=account)

            # register administrator
            if not user.exists():
                return HttpResponseNotFound('你不能自行创建管理员账号！')

            # login
            if user.values('password')[0]['password'] == password:
                return HttpResponse('Successfully login')
            else:
                return HttpResponseNotFound('账号或密码不正确')
        elif user_info['type'] == 'student':
            user = Student.objects.filter(student_id=account)

            # register student
            if not user.exists():
                Student.objects.create(student_id=account, password=password, student_name="STU_"+account, student_money=0)
                return HttpResponse('Successfully create new administrator')

                # login
            if user.values('password')[0]['password'] == password:
                return HttpResponse('Successfully login')
            else:
                return HttpResponseNotFound('账号或密码不正确！')
        else:
            return HttpResponseBadRequest('The type should be student or administrator')
    else:
            return HttpResponseBadRequest('The method should be post')
