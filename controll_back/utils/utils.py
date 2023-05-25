from datetime import timezone
from datetime import datetime
from django.utils.timezone import make_aware

def get_time_from_request(request):
    date = request['date']
    time = request['time']
    tz = timezone.utc
    dt = datetime.strptime(f'{date} {time}', '%Y-%m-%d %H:%M')
    dt_tz = make_aware(dt, tz)
    return dt_tz


def status_sorter(elem):
    if elem['status'] == '进行中':
        return 0
    elif elem['status'] == '未开始':
        return 1
    else:
        return 2