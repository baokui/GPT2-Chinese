import requests
import time
import sys
def main(url0,port):
    t0 = time.time()
    url = url0+port+"/api/gen"
    path_data = 'data/test_text.txt'
    with open(path_data,'r') as f:
        s = f.read().strip().split('\n')
    for str in s:
        data = {"input":str}
        res = requests.post(url=url,json=data)
        #if res.json()['message']!='success':
            #print(res.json())
    t1 = time.time()
    print('number of samles:{},total time:{}s, QPS:{}'.format(len(s),'%0.4f'%(t1-t0),'%0.4f'%(len(s)/(t1-t0))))
if __name__=='__main__':
    port = sys.argv[1]
    url0 = sys.argv[2]
    main(url0,port)