# -*- encoding: utf-8 -*-
from flask import Flask, request, Response
import json
import numpy as np
import gpt_gen
import sys
import logging
from datetime import datetime
import os
from gevent.pywsgi import WSGIServer
from gevent import monkey
from geventwebsocket.handler import WebSocketHandler
import time
monkey.patch_all()
app = Flask(__name__)
app.logger.setLevel(logging.INFO)
port = 5000
style = sys.argv[1]
if style=='poem':
    from Config_poem import config_predict
elif style=='prose':
    from Config_prose import config_predict
else:
    from Config_gou import config_predict
if len(sys.argv)>2:
   port = int(sys.argv[2])
if len(sys.argv)>3:
    gpus = sys.argv[3]
    ConfigPredict = config_predict(gpus=gpus)
else:
    ConfigPredict = config_predict()
batchGenerating=ConfigPredict.batchGenerating
path_configs = ConfigPredict.model_configs
num0 = ConfigPredict.predict_nums
tags = ConfigPredict.tags
rmHFW = ConfigPredict.rmHFW
gpus = ConfigPredict.gpus
#os.environ["CUDA_VISIBLE_DEVICES"]=gpus
model,tokenizer,config,device = gpt_gen.getModel(path_config=path_configs,gpu=gpus)
@app.route('/api/gen_'+style, methods=['POST'])
def test2():
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
        if style=='poem':
            result = gpt_gen.generating_poem(app, data, model, config, tokenizer, device, quick = quick, num = num0,
                                             batchGenerating = batchGenerating, gpu = gpus, fast_pattern = ConfigPredict.fast_pattern)

        else:
            result = gpt_gen.generating(app, data, model, config, tokenizer, device, ConfigPredict, quick=quick,num=num0,
                       removeHighFreqWords=rmHFW,batchGenerating=batchGenerating,gpu=gpus)
        t1 = time.time()
        #app.logger.info('time for : {}'.format(then - now))
        app.logger.info("input:{}".format(data))
        app.logger.info("output:\n{}".format('\n'.join(result)))
        app.logger.info("used time:{} s".format('%0.4f'%(t1-t0)))
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
    #http_server = WSGIServer(('127.0.0.1', port), app, handler_class=WebSocketHandler)
    #http_server.serve_forever()
