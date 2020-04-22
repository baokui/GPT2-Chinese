from flask import Flask,request
from gevent.pywsgi import WSGIServer
from gevent import monkey
import time
import sys
import os
import random
import gpt_gen
from Config_gou import config_predict

port = 6000
if len(sys.argv)>1:
    port = int(sys.argv[1])
if len(sys.argv)>2:
    gpus = sys.argv[2]
    ConfigPredict = config_predict(gpus = gpus)
else:
    ConfigPredict = config_predict()
monkey.patch_all()

batchGenerating=ConfigPredict.batchGenerating
path_configs = ConfigPredict.model_configs
num0 = ConfigPredict.predict_nums
tags = ConfigPredict.tags
rmHFW = ConfigPredict.rmHFW
Gpus = ConfigPredict.gpus.split(',')
Model = []
Tokenizer = []
Config = []
Device = []
for i in range(len(Gpus)):
    #os.environ["CUDA_VISIBLE_DEVICES"]=gpus.split(',')[i]
    model,tokenizer,config,device = gpt_gen.getModel(path_config=path_configs,gpu=Gpus[i])
    Model.append(model)
    Tokenizer.append(tokenizer)
    Config.append(config)
    Device.append(device)

Idx = [i for i in range(len(Gpus))]
quick = False
app = Flask(__name__)
def fun1(tokenizer,data):
    return tokenizer.convert_tokens_to_ids(tokenizer.tokenize(data))
def getTime(n):
    path='log/apptest-post-'+str(n)+'-'
    s = []
    for i in range(n):
        with open(path+str(i)+'.log','r') as f:
            s.append(f.read().strip().split('\n')[-1])
    idx0 = s[0].find(':')
    t0 = [s[i][idx0 - 2:idx0 + 6] for i in range(len(s))]
    t1 = [s[i][idx0 + 8:idx0 + 16] for i in range(len(s))]
    devi = [s[i][-1] for i in range(len(s))]
    T = [(t0[i],t1[i]) for i in range(len(t0))]
    T = sorted(T,key=lambda x:x[0])
    T0 = [[int(t0[6:]),int(t0[3:5]),int(t0[:2])] for (t0,t1) in T]
    T1 = [[int(t1[6:]),int(t1[3:5]),int(t1[:2])] for (t0,t1) in T]
    D = []
    for i in range(len(T0)):
        d = 0
        if T1[i][0]<T0[i][0]:
            t_s = T1[i][0]+60-T0[i][0]
            T1[i][1] -= 1
        else:
            t_s = T1[i][0] - T0[i][0]
        if T1[i][1]<T0[i][1]:
            t_m = T1[i][1]+60-T0[i][1]
            T1[i][2] -= 1
        else:
            t_m = T1[i][1] - T0[i][1]
        t_h = T1[i][2] - T0[i][2]
        d = t_s+60*t_m+3600*t_h
        D.append(d)
    S = ['\t'.join(T[i])+'\t'+str(D[i])+'\t'+devi[i] for i in range(len(T))]
    print('\n'.join(S))
@app.route('/api/gen_test', methods=['POST'])
def test():
    #r = request.json
    #data = r["input"]
    print(request.form.get('input'))
    ii = random.sample(Idx,1)[0]
    model = Model[ii]
    config = Config[ii]
    tokenizer = Tokenizer[ii]
    device = Device[ii]
    gpu = Gpus[ii]
    data = '我们'
    result = ['TEST']
    T0 = time.asctime(time.localtime(time.time()))
    gen = True
    if gen:
        for _ in range(8):
            result = gpt_gen.generating(app, data, model, config, tokenizer, device, ConfigPredict, quick=quick, num=num0,
                                    removeHighFreqWords=rmHFW, batchGenerating=batchGenerating, gpu=gpu)
            #rr = gpt_gen.testFun(app, data, model, config, tokenizer, device, ConfigPredict, quick=quick, num=num0,
                                    #removeHighFreqWords=rmHFW, batchGenerating=batchGenerating, gpu=gpus)
        #result = fun1(tokenizer,data)
        time.sleep(0)
    else:
        time.sleep(5)
    T1 = time.asctime( time.localtime(time.time()) )
    return 'TIME--'+T0[11:19]+'->'+T1[11:19]+'   '+str(model.config.n_ctx)+':'+str(ii)

@app.route('/index')
def beijing():
    return 'Beijing'
if __name__ == '__main__':
    http_server = WSGIServer(('127.0.0.1', port), app)
    http_server.serve_forever()