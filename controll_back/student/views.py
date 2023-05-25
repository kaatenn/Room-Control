import json
import time
import datetime
import decimal

import utils
from decimal import Decimal
from common.models import *
from django.http import HttpResponse, HttpResponseBadRequest
from utils import utils
from django.utils.timezone import make_aware
from datetime import timezone


# Create your views here.
def get_room_info(request):
    result = []
    if request.method == 'GET':
        rooms = Room.objects.all()
        get = request.GET

        for room in rooms:
            dt_tz = utils.get_time_from_request(get)
            com_count = Computer.objects.filter(room_id=room.room_id).count()
            ad_name = Administrator.objects.get(ad_id=room.ad_id_id).ad_name
            ordered_com_count = Record.objects.filter(begin_time=dt_tz, com_id__room_id=room.room_id).count()
            result.append({
                'id': room.room_id,
                'administrator': ad_name,
                'capacity': com_count - ordered_com_count
            })
        result_json = json.dumps(result)
        return HttpResponse(result_json)
    else:
        return HttpResponseBadRequest("Method should be GET")


def get_room_detail(request):
    if request.method == 'GET':
        result = []
        get = request.GET
        room_id = get['room_id']
        dt_tz = utils.get_time_from_request(get)
        computers = Computer.objects.filter(room_id=room_id)
        for computer in computers:
            is_ordered = Record.objects.filter(begin_time=dt_tz, com_id=computer.com_id).count() > 0
            result.append({
                'id': computer.com_id,
                'is_ordered': '已被预约' if is_ordered else '未被预约'
            })
        result_json = json.dumps(result)
        return HttpResponse(result_json)
    else:
        return HttpResponseBadRequest("Method should be GET")


def order_computer(request):
    if request.method == "POST":
        record = request.POST

        t = time.time()
        record_id = int(round(t * 1000))
        dt_tz = utils.get_time_from_request(record)
        student = Student.objects.get(student_id=record['student_id'])
        computer = Computer.objects.get(com_id=record['com_id'])
        type = Type.objects.get(type_id=record['type_id'])
        Record.objects.create(record_id=record_id, student_id=student, com_id=computer, amount=None, type_id=type,
                              begin_time=dt_tz, end_time=None)
        return HttpResponse('预约成功！')
    else:
        return HttpResponseBadRequest("Method should be POST")


def get_user_info(request):
    if request.method == 'GET':
        id = request.GET['id']
        user = Student.objects.get(student_id=id)
        records = Record.objects.filter(student_id=user)
        ordered = []
        for record in records:
            status = ''
            if record.amount != None:
                status = '消费 {:.2f} 元'.format(record.amount)
            elif record.begin_time < make_aware(datetime.datetime.now(), timezone.utc):
                status = '进行中'
            else:
                status = '未开始'
            r = {
                'record_id': record.record_id,
                'com_id': record.com_id_id,
                'date': record.begin_time.strftime("%Y-%m-%d"),
                'time': record.begin_time.strftime("%H:%M"),
                'status': status
            }
            ordered.append(r)
        ordered.sort(key=lambda x: (0 if x['status'] == '进行中' else 1 if x['status'] == '未开始' else 2,
                                    make_aware(datetime.datetime.strptime(x['date'] + " " + x['time'], '%Y-%m-%d %H:%M'),
                                               timezone.utc)))
        result = {
            'info': {
                'name': user.student_name,
                'money': '{:.2f}'.format(user.student_money)
            },
            'ordered': ordered
        }
        json_result = json.dumps(result)
        # clear database
        one_hour_ago = datetime.datetime.now() - datetime.timedelta(hours=1)
        one_hour_ago_tz = make_aware(one_hour_ago, timezone.utc)
        records = Record.objects.filter(begin_time__lte=one_hour_ago, amount=None)
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
        return HttpResponse(json_result)
    else:
        return HttpResponseBadRequest("Method should be GET")


def update_info(request):
    if request.method == "POST":
        post = request.POST
        Student.objects.filter(student_id=post['id']).update(student_name=post['name'])
        return HttpResponse('保存成功')
    else:
        return HttpResponseBadRequest("Method should be POST")


def shutdown(request):
    if request.method == "POST":
        record_id = request.POST['record_id']
        student_id = request.POST['student_id']
        now_tz = make_aware(datetime.datetime.now(), timezone.utc)
        record = Record.objects.filter(record_id=record_id)
        time = ((int)(now_tz.timestamp()) - (int)(record[0].begin_time.timestamp())) // 60
        amount = 0.2 * time
        record.update(end_time=now_tz, amount=amount)
        student = Student.objects.filter(student_id=student_id)
        money = student[0].student_money - Decimal(str(amount))
        money = round(money, 2)
        student.update(student_money=money)
        return HttpResponse('下机成功')
    else:
        return HttpResponseBadRequest("Method should be POST")
