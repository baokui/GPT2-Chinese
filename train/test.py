# -*- encoding: utf-8 -*-
from gpt_gen import *
import random
import json
import logging
import sys
from Config import Config
class config_predict(Config):
    # 定义构造方法
    def __init__(self, model_config='', gpus=''):  # __init__() 是类的初始化方法；它在类的实例化操作后 会自动调用，不需要手动调用；
        super().__init__()
        if gpus:
            self.gpus = gpus
        else:
            self.gpus = '0,1,2,3'
        if model_config:
            self.model_configs = model_config
        else:
            self.model_configs = '../bin/config/config_godText_large1.json'
        self.predict_nums = 5
        self.tags = '(文)'
        self.rmHFW = False
        self.repetition_penalty = 1.2
        self.temperature = 0.6
        self.length = 30
        self.resort = True
        self.style = 'prose'
def getmodel(path_config,gpu='3'):
    from Config import Config
    ConfigPredict = config_predict(model_config=path_config,gpus=gpu)
    path_configs = ConfigPredict.model_configs
    model,tokenizer,config,device = getModel(path_config=path_configs,gpu=gpu)
    config['repetition_penalty'] = ConfigPredict.repetition_penalty
    config['temperature'] = ConfigPredict.temperature
    config['length'] = ConfigPredict.length
    return model,config,tokenizer,ConfigPredict
def modelpredict(model,prefix,tokenizer,config,ConfigPredict,maxNb=5):
    prefix0 = prefix
    punc = '.,?!;\t 。，？！；'
    device = 'cuda'
    n_ctx = model.config.n_ctx
    length = min(60, n_ctx-len(prefix)-1)
    temperature = config['temperature']
    topk = config['topk']
    repetition_penalty = config['repetition_penalty']
    id_msk = tokenizer.convert_tokens_to_ids('[MASK]')
    context_tokens = [id_msk] + tokenizer.convert_tokens_to_ids(tokenizer.tokenize(prefix))
    outs = fast_sample_sequence_batch(model, context_tokens, length, nsamples=maxNb,
                                      temperature=temperature, top_k=topk, repitition_penalty=repetition_penalty,
                                      device=device)
    S = []
    continue_writing = False
    removeHighFreqWords = True
    for out in outs:
        tmptext = untokenization(out, config, tokenizer, punc, continue_writing)
        S.append(tmptext)
    S1 = postprocess(S, prefix0, ConfigPredict, removeHighFreqWords=removeHighFreqWords)
    return S1
def main(path_config,path_source='../bin/data/2020-05-18.txt',path_target='../bin/data/res.json'):
    with open(path_source,'r') as f:
        S = f.read().strip().split('\n')
    Data = [S[i].split('\t')[0] for i in range(100)]
    model,config,tokenizer,ConfigPredict = getmodel(path_config)
    R = []
    for prefix in Data:
        print(prefix)
        if len(prefix)>model.config.n_ctx-2:
            continue
        R0 = modelpredict(model, prefix, tokenizer, config, ConfigPredict)
        r = {'input':prefix,'output':R0}
        R.append(r)
        with open(path_target,'w') as f:
            json.dump(R,f, ensure_ascii=False,indent=4)
if __name__ == "__main__":
    path_config,path_source,path_target = sys.argv[1:4]
    main(path_config,path_source,path_target)

