import requests
import time
import sys
import random
import json
def main(path_data,path_target,path_log):
    with open(path_data,'r') as f:
        Data = f.read().strip().split('\n')
    R = []
    f = open(path_log,'a+')
    idx = 0
    for data in Data:
        user_info = {"input":data,"idx":idx}
        T0 = time.asctime(time.localtime(time.time()))
        r = requests.post("http://127.0.0.1:7000/api/gen_test", data=user_info)
        T1 = time.asctime(time.localtime(time.time()))
        s = r.text.split('\t')
        R.append(json.loads(s[0]))
        t0,t1 = s[1:3]
        f.write('outer:'+'\t'+T0+'\t'+T1+'\n')
        f.write('inter:' + '\t' + t0 + '\t' + t1 + '\n')
    with open(path_target,'w') as f:
        json.dump(R,f,ensure_ascii=False,indent=4)
if __name__=="__main__":
    path_data,path_target,path_log = sys.argv[1:]
    main(path_data,path_target,path_log)