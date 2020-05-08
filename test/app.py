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
app = Flask(__name__)
app.logger.setLevel(logging.INFO)
port = 5000
ConfigPredict = []
from Config_poem import config_predict as config_poem
config_poem0 = config_poem()
ConfigPredict.append(config_poem0)
from Config_poem_ai import config_predict as config_poem_ai
config_poem1 = config_poem_ai()
ConfigPredict.append(config_poem1)
from Config_prose import config_predict as config_prose
ConfigPredict.append(config_prose())
from Config_gou import config_predict as config_gou
ConfigPredict.append(config_gou())
batchGenerating=ConfigPredict[0].batchGenerating
path_configs = [c.model_configs for c in ConfigPredict]
num0 = [c.predict_nums for c in ConfigPredict]
tags = [c.tags for c in ConfigPredict]
rmHFW = [c.rmHFW for c in ConfigPredict]
'''
maxNext = ConfigPredict.maxNext_JLX
path_next = ConfigPredict.path_JLX_next
path_simi = ConfigPredict.path_JLX_simi
D_simi = json.load(open(path_simi,'r',encoding='utf-8'))
D_next = json.load(open(path_next,'r',encoding='utf-8'))
D_simi = {k:json.loads(D_simi[k]) for k in D_simi}
D_next = {k:json.loads(D_next[k]) for k in D_next}
'''
D_simi,D_next,maxNext=[],[],[]
model,tokenizer,config,device = [], [], [], []
for ii in range(len(path_configs)):
    m0,t0,c0,d0 = gpt_gen.getModel(path_config=path_configs[ii],gpu=ConfigPredict[ii].gpus)
    c0['repetition_penalty'] = ConfigPredict[ii].repetition_penalty
    c0['temperature'] = ConfigPredict[ii].temperature
    c0['length'] = ConfigPredict[ii].length
    model.append(m0)
    tokenizer.append(t0)
    config.append(c0)
    device.append(d0)
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
        if data[-3:]=='#hd':
            result_poem = gpt_gen.generating_poem_head(app,data[:-3],model[0],config[0],tokenizer[0],device[0],ConfigPredict[0],num=10,gpu=ConfigPredict[0].gpus)
            result_poem = [r+ConfigPredict[0].tags for r in result_poem]
            result_other = gpt_gen_thread.generating_thread(app, data[:-3], model[-2:], config[-2:], tokenizer[-2:], device[-2:], ConfigPredict[-2:],quick, num0[-2:],
                                                   removeHighFreqWordss=rmHFW[-2:], batchGenerating=batchGenerating,tags=tags[-2:],
                                                  D_simi=D_simi,D_next=D_next,maxNext=maxNext,maxChoice=10)
            result = result_poem+result_other
        elif data[-3:]=='#lv':
            model1, config1, tokenizer1, device1, ConfigPredict1 = model[1:], config[1:], tokenizer[1:], device[1:], ConfigPredict[1:]
            num1,rmHFW1,tags1 = num0[1:],rmHFW[1:],tags[1:]
            result = gpt_gen_thread.generating_thread(app, data[:-3], model1, config1, tokenizer1, device1, ConfigPredict1, quick,num1,
                                                      removeHighFreqWordss=rmHFW1, batchGenerating=batchGenerating,tags=tags1,
                                                      D_simi=D_simi, D_next=D_next, maxNext=maxNext, maxChoice=10)
        elif data[-5:]=='#hdlv':
            result_poem = gpt_gen.generating_poem_head(app,data[:-5],model[1],config[1],tokenizer[1],device[1],ConfigPredict[1],num=10,gpu=ConfigPredict[0].gpus)
            result_poem = [r + ConfigPredict[1].tags for r in result_poem]
            result_other = gpt_gen_thread.generating_thread(app, data[:-5], model[-2:], config[-2:], tokenizer[-2:],device[-2:], ConfigPredict[-2:], quick, num0[-2:],
                                                            removeHighFreqWordss=rmHFW[-2:], batchGenerating=batchGenerating,tags=tags[-2:],
                                                            D_simi=D_simi, D_next=D_next, maxNext=maxNext, maxChoice=10)
            result = result_poem + result_other
        else:
            L = [0,2,3]
            model1, config1, tokenizer1, device1, ConfigPredict1 = [model[t] for t in L], [config[t] for t in L], [tokenizer[t] for t in L], [device[t] for t in L],[ConfigPredict[t] for t in L]
            num1, rmHFW1, tags1 = [num0[t] for t in L], [rmHFW[t] for t in L], [tags[t] for t in L]
            result = gpt_gen_thread.generating_thread(app, data[:-3], model1, config1, tokenizer1, device1,
                                                      ConfigPredict1, quick, num1,removeHighFreqWordss=rmHFW1, batchGenerating=batchGenerating,tags=tags1,
                                                      D_simi=D_simi, D_next=D_next, maxNext=maxNext, maxChoice=10)
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
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    app.run(host="0.0.0.0", port=port)
