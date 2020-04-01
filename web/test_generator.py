import json
import numpy as np
import gpt_gen
import sys
from datetime import datetime
import time
import logging
import os
from Config import config_predict
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
ConfigPredict = config_predict()
batchGenerating=ConfigPredict.batchGenerating
path_configs = ConfigPredict.model_configs
num0 = ConfigPredict.predict_nums
tags = ConfigPredict.tags
rmHFW = ConfigPredict.rmHFW
maxNext = ConfigPredict.maxNext_JLX
path_next = ConfigPredict.path_JLX_next
path_simi = ConfigPredict.path_JLX_simi
quick = False
app = None
def main(path_data,mode,path_config,path_target,topk,temp):
    ii = int(mode)
    model, tokenizer, config, device = gpt_gen.getModel(path_config=path_config)
    config['topk'] = topk
    config['temperature'] = temp
    with open(path_data,'r') as f:
        s = f.read().strip().split('\n')
    D = []
    t0 = time.time()
    for data in s:
        result = []
        for _ in range(1):
            if ii == 1:
                r0 = gpt_gen.generating_poem(app, data, model, config, tokenizer, device, quick,
                                             num0[ii], batchGenerating=batchGenerating)
            else:
                r0 = gpt_gen.generating(app, data, model, config, tokenizer, device, ConfigPredict,
                                        quick=quick, num=num0[ii], removeHighFreqWords=rmHFW[ii],
                                        batchGenerating=batchGenerating)
            r0 = [rr + tags[ii] for rr in r0]
            result.extend(r0)
        d = {'input':data,'outputs':result,'num':len(result)}
        D.append(d)
        with open(path_target,'w') as f:
            json.dump(D,f,ensure_ascii=False,indent=4)
    t1 = time.time()
    print('predict time is {} for parameter topk={}'.format(t1-t0,topk))
if __name__=='__main__':
    mode,path_config,data,path_target = sys.argv[1:5]
    if len(sys.argv)>6:
        topk = int(sys.argv[5])
        temp = float(sys.argv[6])
    else:
        topk = 8
        temp = 1.0
    main(data,mode,path_config,path_target,topk,temp)