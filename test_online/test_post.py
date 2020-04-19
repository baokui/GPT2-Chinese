import requests
url = "http://10.160.25.112:5000/api/gen"
data = '{"input":"ab"}'
res = requests.post(url=url,data=data)
print(res.text)