from django.db import models


class Client(models.Model):
    uid = models.CharField(max_length=200)

    def __str__(self):
        return self.uid


class KusoWifi(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateTimeField()
    comment = models.TextField(max_length=256)

    @staticmethod
    def create_new(uid, date, comment):
        try:
            client = Client.objects.get(uid=uid)
        except Client.DoesNotExist:
            client = Client(uid=uid)
            client.save()

        wifi = KusoWifi(client=client, date=date, comment=comment)
        wifi.save()

    def __str__(self):
        return self.comment
