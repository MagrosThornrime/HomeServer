import requests
import json

url = "http://localhost:5000/sensor_entry"
with open("entry.json", "r") as json_file:
    form = json.load(json_file)
print(form)
result = requests.post(url, data=form)
print(result)
