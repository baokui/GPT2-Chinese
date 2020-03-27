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
quick = False
HFW = [[],[],[],[]]
with open(path_HFW,'r') as f:
    HFW[2] = f.read().strip().split('\n')

def main(data,mode):
    ii = int(mode)
    model, tokenizer, config, device = gpt_gen.getModel(path_config=path_configs[ii])
    result = []
    if ii==1:
        r0 = gpt_gen.generating_poem('a',data, model[ii], config[ii], tokenizer[ii],device[ii],quick,num0[ii],batchGenerating=batchGenerating)
    else:
        r0 = gpt_gen.generating('a',data, model[ii], config[ii], tokenizer[ii],device[ii],quick,num0[ii],removeHighFreqWords=rmHFW[ii],HighFreqWords=HFW[ii],batchGenerating=batchGenerating)
    r0 = [rr + tags[ii] for rr in r0]
    result.extend(r0)
    print('input:%s'%data)
    print('output:\n%s'%'\n'.join(result))
    return result
if __name__=='__main__':
    mode,data = sys.argv[1:3]
    main(data,mode)