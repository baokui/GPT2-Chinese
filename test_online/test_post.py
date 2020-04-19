import requests
url = "http://10.160.25.112:5001/api/gen"
data = {"input":"你好"}
res = requests.post(url=url,json=data)
print(res.json())