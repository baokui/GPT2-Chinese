from flask import Flask
from  gevent.pywsgi import WSGIServer
from gevent import monkey
import time
import sys
import os

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
os.environ["CUDA_VISIBLE_DEVICES"]=gpus
model,tokenizer,config,device = gpt_gen.getModel(path_config=path_configs,gpu=ConfigPredict.gpus)

app = Flask(__name__)
@app.route('/')
def hello_world():
    year = time.localtime().tm_year
    month = time.localtime().tm_mon
    day = time.localtime().tm_mday

    hour = time.localtime().tm_hour
    minute = time.localtime().tm_min
    second = time.localtime().tm_sec

    T0 = '-'.join([str(hour), '时', str(minute), '分', str(second), '秒'])
    time.sleep(10)

    hour = time.localtime().tm_hour
    minute = time.localtime().tm_min
    second = time.localtime().tm_sec

    T1 = '-'.join([str(hour), '时', str(minute), '分', str(second), '秒'])
    return 'Hello World!'+T0+'->'+T1

@app.route('/index')
def beijing():
    return 'Beijing'
if __name__ == '__main__':
    http_server = WSGIServer(('127.0.0.1', port), app)
    http_server.serve_forever()