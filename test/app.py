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
ConfigPredict.append(config_poem())
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
        result = gpt_gen_thread.generating_thread(app, data, model, config, tokenizer, device, ConfigPredict,quick, num0,
                                                   removeHighFreqWordss=rmHFW, batchGenerating=batchGenerating,tags=tags,
                                                  D_simi=D_simi,D_next=D_next,maxNext=maxNext,maxChoice=10)
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
