# -*- encoding: utf-8 -*-
import gpt_gen
from flask import Flask, request, Response
from gevent.pywsgi import WSGIServer
from gevent import monkey
import time
import json

monkey.patch_all()
app = Flask(__name__)

port = 7000
from Config_gou import config_predict
gpus='0'
style='gou'
ConfigPredict = config_predict(gpus=gpus)
batchGenerating=ConfigPredict.batchGenerating
path_configs = ConfigPredict.model_configs
num0 = ConfigPredict.predict_nums
tags = ConfigPredict.tags
rmHFW = ConfigPredict.rmHFW
gpus = ConfigPredict.gpus
model,tokenizer,config,device = gpt_gen.getModel(path_config=path_configs,gpu=gpus)

@app.route('/', methods=['POST'])
def test1():
    r = request.json
    data = r["input"]
    quick = False
    if "quick" in r:
        print("quick pattern")
        if r["quick"]=="True":
            quick = True
    try:
        if style=='poem':
            result = gpt_gen.generating_poem(app, data, model, config, tokenizer, device, quick = quick, num = num0,
                                             batchGenerating = batchGenerating, gpu = gpus, fast_pattern = ConfigPredict.fast_pattern)

        else:
            result = gpt_gen.generating(app, data, model, config, tokenizer, device, ConfigPredict, quick=quick,num=num0,
                       removeHighFreqWords=rmHFW,batchGenerating=batchGenerating,gpu=gpus)
        response = {'message':'success','input':data,'result': result}
    except Exception as e:
        app.logger.error("error:",e)
        response = {'message': 'error', 'input': data, 'result': None}
    response_pickled = json.dumps(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/index', methods=['POST'])
def test2():
    r = request.json
    data = r["input"]
    quick = False
    if "quick" in r:
        print("quick pattern")
        if r["quick"]=="True":
            quick = True
    try:
        if style=='poem':
            result = gpt_gen.generating_poem(app, data, model, config, tokenizer, device, quick = quick, num = num0,
                                             batchGenerating = batchGenerating, gpu = gpus, fast_pattern = ConfigPredict.fast_pattern)

        else:
            result = gpt_gen.generating(app, data, model, config, tokenizer, device, ConfigPredict, quick=quick,num=num0,
                       removeHighFreqWords=rmHFW,batchGenerating=batchGenerating,gpu=gpus)
        response = {'message':'success','input':data,'result': result}
    except Exception as e:
        app.logger.error("error:",e)
        response = {'message': 'error', 'input': data, 'result': None}
    response_pickled = json.dumps(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

if __name__ == "__main__":
    server  = WSGIServer(("0.0.0.0", port), app)
    print("Server started")
    server.serve_forever()
