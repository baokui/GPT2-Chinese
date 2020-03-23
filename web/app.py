# -*- encoding: utf-8 -*-
from flask import Flask, request, Response
import json
import numpy as np
import gpt_gen
import sys
from datetime import datetime
import logging
app = Flask(__name__)
app.logger.setLevel(logging.INFO)
port = 5000
style = 0#0大白狗, 1散文
if len(sys.argv)>1:
   port = int(sys.argv[1])
if len(sys.argv)>2:
   style = int(sys.argv[2])
path_configs = ['config/config_godText_large1.json','config/config_dabaigou.json']
num0 = [10,3]
model,tokenizer,config,device = [], [], [], []
for path_config in path_configs:
    m0,t0,c0,d0 = gpt_gen.getModel(path_config=path_config)
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
        result = []
        for ii in range(len(path_configs)):
            r0 = gpt_gen.generating(app,data, model[ii], config[ii], tokenizer[ii],device[ii],quick,num0[ii])
            result.extend(r0)
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
