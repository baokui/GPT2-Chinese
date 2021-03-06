# -*- encoding: utf-8 -*-
from flask import Flask, request, Response
import json
import torch
import numpy as np
import gpt_gen
import gpt_gen_thread
import sys
from datetime import datetime
import time
import logging
from Config import config_predict
app = Flask(__name__)
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
model,tokenizer,config,device = [], [], [], []
for ii in range(len(path_configs)):
    m0,t0,c0,d0 = gpt_gen.getModel(path_config=path_configs[ii],gpu=ConfigPredict.gpus[ii])
    c0['repetition_penalty'] = ConfigPredict.repetition_penalty[ii]
    c0['temperature'] = ConfigPredict.temperature[ii]
    c0['length'] = ConfigPredict.length[ii]
    model.append(m0)
    tokenizer.append(t0)
    config.append(c0)
    device.append(d0)
D_simi = json.load(open(path_simi,'r',encoding='utf-8'))
D_next = json.load(open(path_next,'r',encoding='utf-8'))
D_simi = {k:json.loads(D_simi[k]) for k in D_simi}
D_next = {k:json.loads(D_next[k]) for k in D_next}
@app.route('/api/gen', methods=['POST'])
def test2():
    r = request.json
    #print(type(r))
    #print(request.json)
    #r = '{"input": "们"}'
    #r = json.loads(r)
    data = r["input"]
    if "num" in r:
        num = r["num"]
    else:
        num = 5
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
        if ConfigPredict.useThread:
            result = gpt_gen_thread.generating_thread(app, data, model, config, tokenizer, device, ConfigPredict,quick, num0,
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
        app.logger.info('used time: {} s'.format('%0.4f'%(t1-t0)))
        then = datetime.now()
        app.logger.info('time: {}'.format(then))
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
    app.run(host="0.0.0.0", port=port)
