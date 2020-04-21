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
@app.route('/api/gen_test', methods=['POST'])
def test():
    a = [model,tokenizer,config,device]
    T0 = time.asctime( time.localtime(time.time()) )
    time.sleep(10)
    T1 = time.asctime( time.localtime(time.time()) )
    return 'Hello World!'+T0+'->'+T1

@app.route('/index')
def beijing():
    return 'Beijing'
if __name__ == '__main__':
    http_server = WSGIServer(('127.0.0.1', port), app)
    http_server.serve_forever()