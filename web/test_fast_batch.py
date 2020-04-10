from gpt_gen import *
import time
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
ConfigPredict = config_predict()
config_predict = ConfigPredict
batchGenerating=ConfigPredict.batchGenerating
path_configs = ConfigPredict.model_configs
num0 = ConfigPredict.predict_nums
tags = ConfigPredict.tags
rmHFW = ConfigPredict.rmHFW
maxNext = ConfigPredict.maxNext_JLX
path_next = ConfigPredict.path_JLX_next
path_simi = ConfigPredict.path_JLX_simi
model,tokenizer,config,device = [], [], [], []
ii=2
gpu = '7'
model,tokenizer,config,device = getModel(path_config=path_configs[ii],gpu=gpu)
prefix = '我们'
#model,config,tokenizer,device,config_predict = model[ii],config[ii],tokenizer[ii],device[ii],ConfigPredict
torch.cuda.set_device(int(gpu))
topk=8
topp=0
repetition_penalty=1.5
length=50
n_ctx = model.config.n_ctx
nsamples = 10
temperature = 0.8
punc = '.,?!;\t 。，？！；'
continue_writing=False
with open('data/test_text.txt','r') as f:
    s = f.read().strip().split('\n')
if 1:
    T0 = []
    T1 = []
    D0 = []
    D1 = []
    for prefix in s:
        t0 = time.time()
        fast_pattern = False
        config['repetition_penalty'] = 1.5
        S = generating(0,prefix,model,config,tokenizer,device,config_predict,quick=False,num=nsamples,continue_writing=False,removeHighFreqWords=False,batchGenerating=True,gpu=gpu,onlyMax=False,fast_pattern=fast_pattern)
        t1 = time.time()
        fast_pattern = True
        config['repetition_penalty'] = 1.2
        S1 = generating(0, prefix, model, config, tokenizer, device, config_predict, quick=False, num=nsamples,
                       continue_writing=False, removeHighFreqWords=False, batchGenerating=True, gpu=gpu, onlyMax=False,
                       fast_pattern=fast_pattern)
        t2 = time.time()
        T0.append(t1-t0)
        T1.append(t2-t1)
        S1 = [t+'(fast)' for t in S1]
        D0.append({'input':prefix,'ouput':S+S1})
        with open('data/result.json','w') as f:
            json.dump(D0,f,ensure_ascii=False,indent=4)
        print(len(T0),np.mean(T0),np.mean(T1))
