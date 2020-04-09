# -*- encoding: utf-8 -*-
import json
import gpt_gen
import gpt_gen_thread
import sys
from Config import config_predict

path_source = sys.argv[1]
path_target = sys.argv[2]
gpus = sys.argv[3].split(',')
repetition_penalty = sys.argv[4]

ConfigPredict = config_predict()
ConfigPredict.gpus = gpus
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
    c0['repetition_penalty'] = repetition_penalty
    model.append(m0)
    tokenizer.append(t0)
    config.append(c0)
    device.append(d0)
D_simi = json.load(open(path_simi,'r',encoding='utf-8'))
D_next = json.load(open(path_next,'r',encoding='utf-8'))
D_simi = {k:json.loads(D_simi[k]) for k in D_simi}
D_next = {k:json.loads(D_next[k]) for k in D_next}
import json
app = 0
def main(path_source,path_target):
    with open(path_source,'r') as f:
        s = f.read().strip().split('\n')
    R = []
    for data in s:
        result = gpt_gen_thread.generating_thread(app, data, model, config, tokenizer, device, ConfigPredict, quick, num0,
                                              removeHighFreqWordss=rmHFW, batchGenerating=batchGenerating, tags=tags,
                                              D_simi=D_simi, D_next=D_next, maxNext=maxNext, maxChoice=10)
        d = {'input':data,'output':result}
        R.append(d)
        if len(R)%5==0:
            with open(path_target,'w') as f:
                json.dump(R,f,ensure_ascii=False,indent=4)
            print('processing %d lines (total %d lines)'%(len(R),len(s)))