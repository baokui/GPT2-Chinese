# -*- encoding: utf-8 -*-
from flask import Flask, request, Response
import json
import numpy as np
import gpt_gen
import gpt_gen_thread
import sys
import time
import logging
import torch
from Config import config_predict
from datetime import datetime
import GPUtil
from gevent.pywsgi import WSGIServer #关键这个
app = Flask(__name__)
#app.run(threaded=True)
#app.run(processes=True)
app.logger.setLevel(logging.INFO)
port = 5000
style = 0#0大白狗, 1散文
if len(sys.argv)>1:
   port = int(sys.argv[1])
ConfigPredict = config_predict()
batchGenerating=ConfigPredict.batchGenerating
path_configs = ConfigPredict.model_configs
num0 = ConfigPredict.predict_nums
tags = ConfigPredict.tags
rmHFW = ConfigPredict.rmHFW
maxNext = ConfigPredict.maxNext_JLX
path_next = ConfigPredict.path_JLX_next
path_simi = ConfigPredict.path_JLX_simi
model,tokenizer,config,device,GPUs = [],[],[],[],[]
ModelIndex = []
for ii in range(len(path_configs)):
    M0,T0,C0,D0 = [],[],[],[]
    gpus = ConfigPredict.gpus[ii].split(',')
    idx = path_configs[ii].index('config_')+len('config_')
    key = path_configs[ii][idx:-5]
    for gpu in gpus:
        m0,t0,c0,d0 = gpt_gen.getModel(path_config=path_configs[ii],gpu=gpu)
        c0['repetition_penalty'] = ConfigPredict.repetition_penalty[ii]
        c0['temperature'] = ConfigPredict.temperature[ii]
        c0['length'] = ConfigPredict.length[ii]
        M0.append(m0)
        T0.append(t0)
        C0.append(c0)
        D0.append(d0)
    model.append(M0)
    tokenizer.append(T0)
    config.append(C0)
    device.append(D0)
    ModelIndex.append([kk for kk in range(len(gpus))])
    GPUs.append(gpus)
D_simi = json.load(open(path_simi,'r',encoding='utf-8'))
D_next = json.load(open(path_next,'r',encoding='utf-8'))
D_simi = {k:json.loads(D_simi[k]) for k in D_simi}
D_next = {k:json.loads(D_next[k]) for k in D_next}
@app.route('/api/gen', methods=['POST'])
def test2():
    modelidx = [np.random.randint(0,len(t)) for t in ModelIndex]
    #gpu_av = GPUtil.getAvailable(order='load', limit=8, maxLoad=0.9, maxMemory=0.9)
    gpu_av = GPUtil.getAvailable(order='memory', limit=8)
    gpu_opt = 0
    if len(gpu_av)>0:
        for i in range(len(gpu_av)):
            for j in range(len(GPUs)):
                if str(gpu_av[i]) in GPUs[j]:
                    gpu_opt = 1
                    modelidx[j] = GPUs[j].index(str(gpu_av[i]))
                    break
    r = request.json
    data = r["input"]
    quick = False
    if "quick" in r:
        print("quick pattern")
        if r["quick"]=="True":
            quick = True
    app.logger.info(data)
    try:
        now = datetime.now()
        app.logger.info('time: {}'.format(now))
        t0 = time.time()
        modl =  [model[ii][modelidx[ii]] for ii in range(len(modelidx))]
        conf = [config[ii][modelidx[ii]] for ii in range(len(modelidx))]
        tokn = [tokenizer[ii][modelidx[ii]] for ii in range(len(modelidx))]
        devi = [device[ii][modelidx[ii]] for ii in range(len(modelidx))]
        ConfigPredict.gpus = [GPUs[ii][modelidx[ii]] for ii in range(len(modelidx))]
        if ConfigPredict.useThread:
            result = gpt_gen_thread.generating_thread(app, data, modl, conf, tokn, devi, ConfigPredict,quick, num0,
                                                       removeHighFreqWordss=rmHFW, batchGenerating=batchGenerating,tags=tags,
                                                      D_simi=D_simi,D_next=D_next,maxNext=maxNext,maxChoice=10)
        else:
            result = []
            for ii in range(len(path_configs)):
                gpu = ConfigPredict.gpus[ii]
                torch.cuda.set_device(int(gpu))
                if ii==1:
                    r0 = gpt_gen.generating_poem(app,data, model[ii], config[ii], tokenizer[ii],device[ii],quick,num0[ii],batchGenerating=batchGenerating,gpu=gpu)
                else:
                    r0 = gpt_gen.generating(app,data, model[ii], config[ii], tokenizer[ii],device[ii],ConfigPredict,quick=quick,num=num0[ii],removeHighFreqWords=rmHFW[ii],batchGenerating=batchGenerating,gpu=gpu)
                r0 = [rr + tags[ii] for rr in r0]
                result.extend(r0)
            result_nnlm = gpt_gen.nnlm_modelpredict(D_simi,D_next,ConfigPredict,inputStr=data,maxNext=maxNext,maxChoice=10,num=num)
            result += [tmp+tags[-1] for tmp in result_nnlm]
        t1 = time.time()
        modelidx_s = ','.join([str(t) for t in ConfigPredict.gpus])
        app.logger.info('gpus {}-th (opt is {}) string and use time: {} s'.format(modelidx_s,gpu_opt,'%0.4f'%(t1-t0)))
        #app.logger.info('time for : {}'.format(then - now))
        app.logger.info("input:{}".format(data))
        app.logger.info("output:\n{}".format('\n'.join(result)))
        response = {'message':'success','input':data,'result': result}
    except Exception as e:
        app.logger.error("error:",e)
        response = {'message': 'error', 'input': data, 'result': None}
    response_pickled = json.dumps(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

# start flask app
if __name__ == '__main__':
    #app.run(threaded=True)
    app.run(host="0.0.0.0", port=port)
    #WSGIServer(('127.0.0.1', port), app).serve_forever()
