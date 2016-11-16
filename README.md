# kuso-wifi-server
某大学のWifiに対するヘイトがここに集う

## Install
```sh
docker-compose up -d
docker exec -it <app_container_name> python manage.py makemigrations kuso_wifi_server && python manage.py migrate
```
