import requests
import time
def main():
    t0 = time.time()
    url = "http://10.160.25.112:5001/api/gen"
    path_data = 'data/test_parallel.txt'
    with open(path_data,'r') as f:
        s = f.read().strip().split('\n')
    for str in s:
        data = {"input":str}
        res = requests.post(url=url,json=data)
        if res.json()['message']!='success':
            print(res.json())
    t1 = time.time()
    print('number of samles:{},total time:{}s, QPS:{}'.format(len(s),'%0.4f'%(t1-t0),'%0.4f'%(len(s)/(t1-t0))))
