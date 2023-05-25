import json
import time
import datetime
import decimal

import utils
from django.http.request import QueryDict
from decimal import Decimal
from common.models import *
from django.http import HttpResponse, HttpResponseBadRequest
from utils import utils
from django.utils.timezone import make_aware
from datetime import timezone
from django.db.models import Max


def get_administrator_info(request):
    # clear database
    one_hour_ago = datetime.datetime.now() - datetime.timedelta(hours=1)
    one_hour_ago_tz = make_aware(one_hour_ago, timezone.utc)
    records = Record.objects.filter(begin_time__lte=one_hour_ago_tz, amount=None)
    students = []
    for r in records:
        students.append(record.student_id_id)
        r.end_time = record.begin_time + datetime.timedelta(hours=1)
        r.amount = 12
        r.save()
    for stu in students:
        stu_r = Student.objects.filter(student_id=stu)
        money = stu_r[0].student_money - Decimal(str(12))
        money = round(money, 2)
        stu_r.update(student_money=money)

    # get info
    if request.method == "GET":
        id = request.GET['account']
        administrator = Administrator.objects.get(ad_id=id)
        rooms = Room.objects.filter(ad_id=administrator)
        rooms_result = []
        amount_sum = 0
        now = make_aware(datetime.datetime.now(), timezone.utc)
        today = datetime.datetime.today().date()
        today_start = make_aware(datetime.datetime.combine(today, datetime.time.min), timezone.utc)
        for room in rooms:
            com = Computer.objects.filter(room_id=room)
            records = Record.objects.filter(begin_time__lte=now, begin_time__gte=today_start, com_id__in=com).exclude(amount=None)
            amount_room = 0
            for record in records:
                amount_room += float(record.amount)
            amount_sum += amount_room
            rooms_result.append({
                'room_id': room.room_id,
                'com_count': com.count(),
                'room_amount': '%.2f' % amount_room
            })
        info = {
            'name': administrator.ad_name,
            'ad_amount': '%.2f' % amount_sum
        }
        result = {
            'info': info,
            'rooms': rooms_result
        }
        return HttpResponse(json.dumps(result))
    else:
        return HttpResponseBadRequest("Method should be POST")


def update_info(request):
    if request.method == "POST":
        post = request.POST
        Administrator.objects.filter(ad_id=post['id']).update(ad_name=post['name'])
        return HttpResponse('保存成功')
    else:
        return HttpResponseBadRequest("Method should be POST")


def add_computer(request):
    if request.method == "POST":
        room_id = request.POST['room_id']
        room = Room.objects.get(room_id=room_id)
        max_com_id = Computer.objects.filter(room_id=room).aggregate(Max('com_id'))['com_id__max']
        last_part = max_com_id.split('-')[-1]
        new_last_part = ('0' if int(last_part) + 1 < 10 else '') + str(int(last_part) + 1)
        new_com_id = max_com_id[:-len(last_part)] + new_last_part
        Computer.objects.create(com_id=new_com_id, room_id=room)
        return HttpResponse('添加成功')
    else:
        return HttpResponseBadRequest("Method should be POST")


def delete_computer(request):
    if request.method == 'DELETE':
        delete = QueryDict(request.body)
        room_id = delete['room_id']
        room = Room.objects.get(room_id=room_id)
        max_com_id = Computer.objects.filter(room_id=room).aggregate(Max('com_id'))['com_id__max']
        Computer.objects.get(com_id=max_com_id).delete()
        return HttpResponse('删除成功')
    else:
        return HttpResponseBadRequest("Method should be DELETE")
