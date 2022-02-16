import requests


BASE = "http://127.0.0.1:8001/"

# response = requests.get(BASE + "helloworld/tim/19")
# print(response.json())

response = requests.get(BASE + "helloworld/tim")
print(response.json())
response = requests.get(BASE + "helloworld/bill")
print(response.json())

# response = requests.post(BASE + "helloworld")
# print(response.json())

response = requests.put(BASE + "helloworld/bill", {})
print(response.json())

