import requests
import json

r = requests.post('http://10.0.18.18:5000/bot', data={"bullshit":"sucks"})

print r.json()