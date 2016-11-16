# kuso-wifi-server
某大学のWifiに対するヘイトがここに集う

## Install
取り急ぎ
.env を編集  
SECRET_KEY='secret-key'  
DB_NAME=postgres  
DB_USER=postgres  
DB_PASS=postgres  
DB_SERVICE=postgres  
DB_PORT=5432  
DEBUG=true  


```sh
docker-compose up -d
docker exec -it <app_container_name> python manage.py makemigrations kuso_wifi_server && python manage.py migrate
```
