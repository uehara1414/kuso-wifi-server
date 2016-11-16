from django.contrib import admin
from .models import Client, Wifi, WifiReport
# Register your models here.

admin.site.register(Client)
admin.site.register(Wifi)
admin.site.register(WifiReport)