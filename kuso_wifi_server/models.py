from django.db import models


class Client(models.Model):
    uid = models.CharField(max_length=200)

    def __str__(self):
        return self.uid


class KusoWifi(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    ssid = models.CharField(max_length=64, default="unknown")
    date = models.DateTimeField()
    ping_ms = models.IntegerField(default=0)
    comment = models.TextField(max_length=256)

    @staticmethod
    def create_new(uid, ssid, date, ping_ms, comment):
        try:
            client = Client.objects.get(uid=uid)
        except Client.DoesNotExist:
            client = Client(uid=uid)
            client.save()

        wifi = KusoWifi(client=client, ssid=ssid, date=date, ping_ms=ping_ms, comment=comment)
        wifi.save()

    def __str__(self):
        return self.comment

    @staticmethod
    def get_one_day(year, month, day):
        return KusoWifi.objects.filter(date__year=year, date__month=month, date__day=day)

    @staticmethod
    def count_kuso_wifi():
        ret = []
        date_set = KusoWifi.objects.dates('date', 'day')
        for date in date_set:
            count = len(KusoWifi.objects.filter(date__year=date.year, date__month=date.month, date__day=date.day))
            dct = {'date': date, 'count': count}
            ret.append(dct)
        return ret
