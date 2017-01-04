import requests
import datetime

def post_new(comment="comment"):
    date = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    data = {
        "uid": "aaa",
        "ssid": "dummy-wifi",
        "date": date,
        "ping": 200,
        "comment": comment
    }
    return requests.post("http://localhost:8080/honto-kuso/", json=data)
