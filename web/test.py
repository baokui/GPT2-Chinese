import json
import numpy as np
import gpt_gen
import sys
from datetime import datetime
import time
import logging

batchGenerating=True
path_HFW = '../data/words_highFreq.txt'
path_configs = ['config/config_godText_large1.json','config/config_poem.json','config/config_dabaigou.json']
num0 = [8,4,4]
tags = ['(文)','(诗)','(大白狗)','(句联想)']
rmHFW = [False,False,True,False]
maxNext = 3
path_next = 'model/nnlm/D_next.json'
path_simi = 'model/nnlm/D_simi.json'

HFW = [[],[],[],[]]
with open(path_HFW,'r') as f:
    HFW[2] = f.read().strip().split('\n')
model,tokenizer,config,device = [], [], [], []
for path_config in path_configs:
    m0,t0,c0,d0 = gpt_gen.getModel(path_config=path_config)
    model.append(m0)
    tokenizer.append(t0)
    config.append(c0)
    device.append(d0)
D_simi = json.load(open(path_simi,'r',encoding='utf-8'))
D_next = json.load(open(path_next,'r',encoding='utf-8'))
D_simi = {k:json.loads(D_simi[k]) for k in D_simi}
D_next = {k:json.loads(D_next[k]) for k in D_next}

def main(data):
    result = []
    for ii in range(len(path_configs)):
        if ii==1:
            r0 = gpt_gen.generating_poem('a',data, model[ii], config[ii], tokenizer[ii],device[ii],quick,num0[ii],batchGenerating=batchGenerating)
        else:
            r0 = gpt_gen.generating('a',data, model[ii], config[ii], tokenizer[ii],device[ii],quick,num0[ii],removeHighFreqWords=rmHFW[ii],HighFreqWords=HFW[ii],batchGenerating=batchGenerating)
        r0 = [rr + tags[ii] for rr in r0]
        result.extend(r0)
    result_nnlm = gpt_gen.nnlm_modelpredict(D_simi,D_next,inputStr=data,maxNext=maxNext,maxChoice=10,num=num)
    result += [tmp+tags[-1] for tmp in result_nnlm]
    print('input:%s'%data)
    print('output:\n%s'%'\n'.join(result))
    return result
if __name__=='__main__':
    data = sys.argv[1]
    main(data)