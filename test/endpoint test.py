import requests
import json

r = requests.post('http://10.16.1.185:5000/bot', data=json.dumps({"name":"lukas"}))

print r