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
            ssid = data['ssid']
        except KeyError:
            return JsonResponse({"message": "ssid param is missing."})
        except Exception as e:
            return JsonResponse({"message": str(e)})

        try:
            ping_ms = data['ping']
        except KeyError:
            return JsonResponse({"message": "ping param is missing."})
        except Exception as e:
            return JsonResponse({"message": str(e)})

        try:
            KusoWifi.create_new(uid, ssid, date, ping_ms, message)
        except Exception as e:
            return JsonResponse({"message": "Validation Error: " + str(e)})

        return JsonResponse({"message": "ok"})

    else:
        return JsonResponse({"message": "POST please."})

@csrf_exempt
def post_filter_settings(request):
    data = json.loads(request.body.decode("utf-8"))
    filter_ssid_set = set()
    for ssid in data["ssid"]:
        filter_ssid_set.add(ssid)
    request.session['filter_ssid'] = list(filter_ssid_set)
    return JsonResponse({"message": "ok"})


class ListView(generic.ListView):
    model = KusoWifi
    template_name = "kuso_wifi_server/list.html"

    def get_queryset(self):
        return KusoWifi.objects.order_by('-date')


def index(request):
    kuso_wifi_calendar = KusoWifi.count_kuso_wifi()
    timeline = KusoWifi.objects.filter(ssid__in=request.session.get('filter_ssid', [])).order_by('-date')[:30]
    return render(request, "kuso_wifi_server/index.html", {"dates": kuso_wifi_calendar, "timeline": timeline})


def ssid_ajax(request):
    all_wifi_set = KusoWifi.get_ssid_set()
    filtered_wifi_list = request.session.get('filter_ssid', [])
    wifi_list = []
    for wifi in all_wifi_set:
        wifi_list.append({wifi: wifi in filtered_wifi_list})
    return JsonResponse(wifi_list)


def one_day_view(request, year, month, day):
    wifis = KusoWifi.get_one_day(year, month, day)
    hour_list = []
    for hour in range(24):
        cnt = len(wifis.filter(date__hour=hour))
        one = {"hour": hour, "cnt": cnt}
        hour_list.append(one)
    return render(request, "kuso_wifi_server/one_day_kuso.html", {"kusowifi_list": wifis, "hour_list": hour_list})