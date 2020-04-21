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
monkey.patch_all()

ConfigPredict = config_predict()
batchGenerating=ConfigPredict.batchGenerating
path_configs = ConfigPredict.model_configs
num0 = ConfigPredict.predict_nums
tags = ConfigPredict.tags
rmHFW = ConfigPredict.rmHFW
gpus = ConfigPredict.gpus
Model = []
Tokenizer = []
Config = []
Device = []
for i in range(len(gpus.split(','))):
    os.environ["CUDA_VISIBLE_DEVICES"]=gpus.split(',')[i]
    model,tokenizer,config,device = gpt_gen.getModel(path_config=path_configs,gpu=ConfigPredict.gpus)
    Model.append(model)
    Tokenizer.append(tokenizer)
    Config.append(config)
    Device.append(device)
Idx = [i for i in range(len(gpus.split(',')))]
quick = False
app = Flask(__name__)
def fun1(tokenizer,data):
    return tokenizer.convert_tokens_to_ids(tokenizer.tokenize(data))
@app.route('/api/gen_test', methods=['POST'])
def test():
    #r = request.json
    #data = r["input"]
    ii = random.sample(Idx,1)[0]
    model = Model[ii]
    config = Config[ii]
    tokenizer = Tokenizer[ii]
    device = Device[ii]
    data = '我们'
    T0 = time.asctime(time.localtime(time.time()))
    for _ in range(20):
        result = gpt_gen.generating(app, data, model, config, tokenizer, device, ConfigPredict, quick=quick, num=num0,
                                removeHighFreqWords=rmHFW, batchGenerating=batchGenerating, gpu=gpus)
    #result = fun1(tokenizer,data)
    #time.sleep(5)
    T1 = time.asctime( time.localtime(time.time()) )
    return 'Hello World!'+T0[11:19]+'->'+T1[11:19]+':'+str(model.config.n_ctx)+':'+str(result[0])

@app.route('/index')
def beijing():
    return 'Beijing'
if __name__ == '__main__':
    http_server = WSGIServer(('127.0.0.1', port), app)
    http_server.serve_forever()