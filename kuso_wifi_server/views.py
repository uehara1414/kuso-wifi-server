import json
from datetime import datetime

from django.shortcuts import render
from django.http import JsonResponse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from .models import Wifi, WifiReport


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
            WifiReport.create_new(uid, ssid, date, ping_ms, message)
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
    request.session['filter_wifi'] = list(filter_ssid_set)
    return JsonResponse({"message": "ok"})


def index(request):
    filter_wifi = Wifi.objects.filter(ssid__in=request.session.get('filter_wifi', []))
    kuso_wifi_calendar = WifiReport.count_daily_wifi_report(filter_wifi)
    timeline = WifiReport.objects.filter(wifi__in=filter_wifi).order_by('-date')[:30]
    context = {"dates": kuso_wifi_calendar, "timeline": timeline, "filter_ssid": get_ssid_context(request)}
    return render(request, "kuso_wifi_server/index.html", context)


def ssid_ajax(request):
    all_wifi_set = Wifi.objects.all()
    filtered_wifi_list = request.session.get('filter_wifi', [])
    wifi_list = []
    for wifi in all_wifi_set:
        wifi_list.append({wifi.ssid: wifi in filtered_wifi_list})
    return JsonResponse(wifi_list)


def get_ssid_context(request):
    all_wifi_set = Wifi.objects.all()
    filtered_wifi_list = Wifi.objects.filter(ssid__in=request.session.get('filter_wifi', []))
    wifi_list = []
    for wifi in sorted(all_wifi_set):
        wifi_list.append({"name": wifi.ssid, "checked": wifi in filtered_wifi_list})
    return wifi_list


def one_day_report(request, year, month, day):
    filter_wifi = Wifi.objects.filter(ssid__in=request.session.get('filter_wifi', []))
    wifi_report_list = WifiReport.objects.filter(date__year=year, date__month=month, date__day=day, wifi__in=filter_wifi)
    hour_list = []
    for hour in range(24):
        cnt = len(wifi_report_list.filter(date__hour=hour))
        one = {"hour": hour, "cnt": cnt}
        hour_list.append(one)
    return render(request, "kuso_wifi_server/one_day_kuso.html", {"kusowifi_list": wifi_report_list, "hour_list": hour_list, "filter_ssid": get_ssid_context(request)})