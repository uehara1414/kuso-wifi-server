from django.db import models


class Client(models.Model):
    uid = models.CharField(max_length=200)

    @staticmethod
    def get_or_create_new(uid):
        try:
            client = Client.objects.get(uid=uid)
        except Client.DoesNotExist:
            client = Client(uid=uid)
            client.save()
        return client

    def __str__(self):
        return self.uid


class Wifi(models.Model):
    ssid = models.CharField(max_length=64, default="unknown")

    @staticmethod
    def get_or_create_new(ssid):
        try:
            wifi = Wifi.objects.get(ssid=ssid)
        except Wifi.DoesNotExist:
            wifi = Wifi(ssid=ssid)
            wifi.save()
        return wifi

    def __str__(self):
        return self.ssid


    def __lt__(self, other):
        return self.ssid < other.ssid


class WifiReport(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    wifi = models.ForeignKey(Wifi, on_delete=models.CASCADE)
    date = models.DateTimeField()
    ping_ms = models.IntegerField(default=0)
    comment = models.TextField(max_length=256)

    @staticmethod
    def create_new(uid, ssid, date, ping_ms, comment):
        client = Client.get_or_create_new(uid=uid)
        wifi = Wifi.get_or_create_new(ssid=ssid)
        wifi_report = WifiReport(client=client, wifi=wifi, date=date, ping_ms=ping_ms, comment=comment)
        wifi_report.save()

    def __str__(self):
        return str(self.date) + str(self.wifi) + self.comment

    @staticmethod
    def count_daily_wifi_report(filter_wifi=None):
        if filter_wifi is None:
            wifi = Wifi.objects.all()
        ret = []
        date_set = WifiReport.objects.dates('date', 'day')
        for date in date_set:
            count = len(WifiReport.objects.filter(date__year=date.year, date__month=date.month, date__day=date.day, wifi__in=filter_wifi))
            dct = {'date': date, 'count': count}
            ret.append(dct)
        return ret
