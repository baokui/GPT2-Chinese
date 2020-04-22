import requests
import time
import sys
import random
import json
def main_gen(path_data,path_target,path_log):
    with open(path_data,'r',encoding='utf-8') as f:
        Data = f.read().strip().split('\n')
    R = []
    f = open(path_log,'a+')
    for data in Data:
        idx = random.randint(0,10)
        user_info = {"input":data,"idx":idx}
        T0 = time.asctime(time.localtime(time.time()))[11:19]
        r = requests.post("http://127.0.0.1:7000/api/gen_test", data=user_info)
        T1 = time.asctime(time.localtime(time.time()))[11:19]
        s = r.text.split('\t')
        R.append(json.loads(s[0]))
        t0,t1 = s[1:3]
        f.write('outer:'+'\t'+T0+'\t'+T1+'\t'+'inter:' + '\t' + t0 + '\t' + t1 + '\n')
    with open(path_target,'w',encoding='utf-8') as f:
        json.dump(R,f,ensure_ascii=False,indent=4)
def main_test(path_data,path_target,path_log):
    for i in range(10):
        idx = random.randint(0,10)
        user_info = {"input":str(idx),"idx":idx}
        T0 = time.asctime(time.localtime(time.time()))[11:19]
        r = requests.post("http://127.0.0.1:7000/api/gen_test", data=user_info)
        T1 = time.asctime(time.localtime(time.time()))[11:19]
        s = r.text.split('\t')
        t0,t1 = s[1:3]
        print('\t'.join([T0,T1,t0,t1]))
if __name__=="__main__":
    path_data,path_target,path_log,mode = sys.argv[1:]
    if mode=='test':
        main_test(path_data,path_target,path_log)
    if mode=='gen':
        main_gen(path_data,path_target,path_log)