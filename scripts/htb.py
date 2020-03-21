

import requests

url = 'https://www.hackthebox.eu/api/invite/generate'

x = requests.post(url, data = {"asdf":1} , json={"asdf":1, "add":{"asdf":1}}, auth = ("user",'pass'), stream = True)

print(x.content)

print(x.text)

print(x.json())
