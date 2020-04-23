# coding=utf-8
from flask import Flask,request
import requests
from gevent.pywsgi import WSGIServer
from gevent import monkey
import time
import sys
import random
import numpy as np
import json
port,mode,nb_server = sys.argv[1:]
port = int(port)
nb_server = int(nb_server)
monkey.patch_all()
urlList = ["http://127.0.0.1:200"+str(i)+"/api/gen_"+mode for i in range(nb_server)]
Idx = [i for i in range(nb_server)]
app = Flask(__name__)
def getTime(n):
    path='log/apptest-post-'+str(n)+'-'
    def getdata(tag):
        idx0 = [s[i].find(tag)+len(tag) for i in range(n)]
        t0 = [s[i][idx0[i]:idx0[i] + 8] for i in range(len(s))]
        t1 = [s[i][idx0[i] + 10:idx0[i] + 18] for i in range(len(s))]
        T = [(t0[i], t1[i]) for i in range(len(t0))]
        T = sorted(T, key=lambda x: x[0])
        T0 = [[int(t0[6:]), int(t0[3:5]), int(t0[:2])] for (t0, t1) in T]
        T1 = [[int(t1[6:]), int(t1[3:5]), int(t1[:2])] for (t0, t1) in T]
        D = []
        for i in range(len(T0)):
            d = 0
            if T1[i][0] < T0[i][0]:
                t_s = T1[i][0] + 60 - T0[i][0]
                T1[i][1] -= 1
            else:
                t_s = T1[i][0] - T0[i][0]
            if T1[i][1] < T0[i][1]:
                t_m = T1[i][1] + 60 - T0[i][1]
                T1[i][2] -= 1
            else:
                t_m = T1[i][1] - T0[i][1]
            t_h = T1[i][2] - T0[i][2]
            d = t_s + 60 * t_m + 3600 * t_h
            D.append(d)
        return T,D
    s = []
    for i in range(n):
        with open(path+str(i)+'.log','r') as f:
            s.append(f.read().strip().split('\n')[-1])
    devi = [s[i][-1] for i in range(len(s))]
    tag0 = 'TIME--'
    T,D = getdata(tag0)
    tag1 = 'post-time:'
    T1, D1 = getdata(tag1)
    S = ['\t'.join(T[i])+'\t'+str(D[i])+'\t'+devi[i] for i in range(len(T))]
    S1 = ['\t'.join(T1[i]) + '\t' + str(D1[i]) + '\t' + devi[i] for i in range(len(T1))]
    aver_time = sum(D)/len(D)
    aver_time1 = sum(D1)/len(D1)
    print('innerpro:')
    print('\n'.join(S))
    print('post-time:')
    print('\n'.join(S1))
    print('result-inner:average time = {}s,total posts = {},qps = {}'.format(np.mean(D),len(D),len(D)/np.mean(D)))
    print('result-outer:average time = {}s,total posts = {},qps = {}'.format(np.mean(D1),len(D1),len(D1)/np.mean(D1)))
@app.route('/api/gen_test', methods=['POST'])
def test():
    inputData = request.json
    ii = random.sample(Idx,1)[0]
    T0 = time.asctime(time.localtime(time.time()))
    try:
        url = urlList[ii]
        r = requests.post(url, json=inputData)
        R = r.text
        time.sleep(0)
    except:
        #gpt_gen.testFun1()
        inputStr = inputData['input']
        R = {'input': inputStr, 'output': [], "message": "failed"}
        R = json.dumps(R)
        time.sleep(0)
    T1 = time.asctime(time.localtime(time.time()))
    log0 = [R,T0[11:19],T1[11:19]]
    return '\t'.join(log0)
if __name__ == '__main__':
    #app.run(host="0.0.0.0", port=port)
    http_server = WSGIServer(('127.0.0.1', port), app)
    http_server.serve_forever()