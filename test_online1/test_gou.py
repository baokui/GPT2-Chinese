import requests
import time
import sys
import json
def main(url0,port):
    t0 = time.time()
    url = url0+port+"/api/gen_gou"
    path_data = '../test_online/data/test_text10.txt'
    with open(path_data,'r',encoding='utf-8') as f:
        s = f.read().strip().split('\n')
    D = []
    for i in range(len(s)):
        data = {"input":s[i]}
        res = requests.post(url=url,json=data)
        d = {'input':res.json()['input'],'output':res.json()['result']}
        D.append(d)
        #if res.json()['message']!='success':
            #print(res.json())
    t1 = time.time()
    print('number of samles:{},total time:{}s, QPS:{}'.format(len(s),'%0.4f'%(t1-t0),'%0.4f'%(len(s)/(t1-t0))))
    with open('result/tmp'+str(int(time.time()%10000))+'.json','w',encoding='utf-8') as f:
        json.dump(D,f,ensure_ascii=False,indent=4)
if __name__=='__main__':
    port = sys.argv[1]
    url0 = sys.argv[2]
    main(url0,port)