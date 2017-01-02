# kuso-wifi-server
某大学のWifiに対するヘイトがここに集う

## Development

Clone
```sh
git clone https://github.com/uehara1414/kuso-wifi-server.git
cd kuso-wifi-server
```

.env を追加
```
SECRET_KEY='secret-key'
DB_NAME=postgres
DB_USER=postgres
DB_PASS=postgres
DB_SERVICE=postgres
DB_PORT=5432
DEBUG=true
```

コンテナの起動 & データベースの初期化
```sh
docker-compose up -d
docker-compose run web bash
python manage.py migrate
```

お好みのブラウザで http://localhost:8080 にアクセス


## Deploy

上記同様に Clone & .env 追加

コンテナ起動
```sh
docker-compose -f production.yml up -d
docker-compose run web bash
python manage.py migrate
```

アプリが 8080 番ポートにデプロイされるので、お好みのウェブサーバーで 8080 番ポートに適宜プロキシする
