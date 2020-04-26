# -*- encoding: utf-8 -*-
import json
import gpt_gen
import gpt_gen_thread
import sys

nb_models = sys.argv[1]
ConfigPredict = []
from Config_compare import *
ConfigPredict.append(config_predict0())
ConfigPredict.append(config_predict1())
if nb_models=='3':
    ConfigPredict.append(config_predict2())
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
def predict(Data):
    quick = False
    R = []
    app = ''
    for data in Data:
        result = gpt_gen_thread.generating_thread(app, data, model, config, tokenizer, device, ConfigPredict,quick, num0,
                                                   removeHighFreqWordss=rmHFW, batchGenerating=batchGenerating,tags=tags,
                                                  D_simi=D_simi,D_next=D_next,maxNext=maxNext,maxChoice=10)

        R.append({'input':data,'output':result})
    return R
def main(path_source,path_target):
    with open(path_source,'r',encoding='utf-8') as f:
        s = f.read().strip().split('\n')
    R = predict(s)
    with open(path_target,'w',encoding='utf-8') as f:
        json.dump(R,f,ensure_ascii=False,indent=4)
# start flask app
if __name__ == '__main__':
    path_source,path_target = sys.argv[2:4]
    main(path_source,path_target)
