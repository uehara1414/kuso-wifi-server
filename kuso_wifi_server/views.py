import json
from datetime import datetime

from django.shortcuts import render
from django.http import JsonResponse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from .models import KusoWifi


@csrf_exempt
def ajax_post(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))

        try:
            uid = data['uid']
        except Exception as e:
            return JsonResponse({"message": "uid param is missing."})

        try:
            date = data['date']
            date = datetime.strptime(date, '%Y/%m/%d %H:%M:%S')
        except KeyError as e:
            return JsonResponse({"message": "date param is missing."})
        except Exception as e:
            return JsonResponse({"message": str(e)})

        try:
            message = data['comment']
        except Exception as e:
            return JsonResponse({"message": "comment param is missing. If the user comment is empty, set an empty string"})

        try:
            KusoWifi.create_new(uid, date, message)
        except Exception as e:
            return JsonResponse({"message": "Validation Error: " + str(e)})

        return JsonResponse({"message": "ok"})

    else:
        return JsonResponse({"message": "POST please."})


class ListView(generic.ListView):
    model = KusoWifi
    template_name = "kuso_wifi_server/list.html"

    def get_queryset(self):
        return KusoWifi.objects.order_by('-date')


def index(request):
    kuso_wifi_calendar = KusoWifi.count_kuso_wifi()
    return render(request, "kuso_wifi_server/index.html", {"dates": kuso_wifi_calendar})


def one_day_view(request, year, month, day):
    wifis = KusoWifi.get_one_day(year, month, day)
    hour_list = []
    for hour in range(24):
        cnt = len(wifis.filter(date__hour=hour))
        one = {"hour": hour, "cnt": cnt}
        hour_list.append(one)
    return render(request, "kuso_wifi_server/one_day_kuso.html", {"kusowifi_list": wifis, "hour_list": hour_list})