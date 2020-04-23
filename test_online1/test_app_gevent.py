import requests
import time
import sys
import random
import json
def main_gen(path_data,path_target,path_log,sym=''):
    with open(path_data,'r',encoding='utf-8') as f:
        Data = f.read().strip().split('\n')
    R = []
    f = open(path_log,'a+')
    TT0 = 0
    for data in Data:
        idx = random.randint(0,10)
        user_info = {"input":data,"idx":idx}
        T0 = time.asctime(time.localtime(time.time()))[11:19]
        z0 = time.time()
        r = requests.post("http://127.0.0.1:7000/"+sym, json=user_info)
        z1 = time.time()
        TT0 = TT0+z1-z0
        T1 = time.asctime(time.localtime(time.time()))[11:19]
        s = r.text.split('\t')
        R.append(json.loads(s[0]))
        t0,t1 = s[1:3]
        f.write('outer:'+'\t'+T0+'\t'+T1+'\t'+'inter:' + '\t' + t0 + '\t' + t1 + '\n')
    with open(path_target,'w',encoding='utf-8') as f:
        json.dump(R,f,ensure_ascii=False,indent=4)
    s0 = '%0.4f'%TT0
    s1 = '%0.4f'%(len(Data)/TT0)
    print(path_log+': total samples:{}, total time:{}s, qps:{}'.format(len(Data),s0,s1))
if __name__=="__main__":
    path_data,path_target,path_log,mode = sys.argv[1:]
    main_gen(path_data,path_target,path_log,mode)