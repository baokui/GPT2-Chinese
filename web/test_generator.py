import json
import numpy as np
import gpt_gen
import sys
from datetime import datetime
import time
import logging
def generating(app,prefix,model,config,tokenizer,device,quick=False,num=5,continue_writing=False,removeHighFreqWords=False,HighFreqWords=[],batchGenerating=False):
    #print("start:",prefix)
    punc = '.,?!;\t 。，？！；'
    global a
    a = app
    n_ctx = model.config.n_ctx
    fast_pattern = False
    if config['fast_pattern']=="True":
        fast_pattern = True
    length = config['length']
    nsamples = num
    batch_size = config['batch_size']
    temperature = config['temperature']
    topk = config['topk']
    topp = config['topp']
    quick_pattern = quick
    repetition_penalty = config['repetition_penalty']
    if length == -1:
        length = model.config.n_ctx
    raw_text = prefix
    context_tokens = tokenizer.convert_tokens_to_ids(tokenizer.tokenize(raw_text))
    print('test0-%d'%nsamples)
    if batchGenerating:
        S = []
        outs = sample_sequence_batch(model, context_tokens, length, n_ctx, tokenizer, nsamples, temperature=temperature,
                                     top_k=topk,
                                     top_p=topp, repitition_penalty=repetition_penalty,
                                     device=device)
        print('test1-%d'%len(outs))
        for out in outs:
            tmptext = untokenization(out, config, tokenizer, punc, continue_writing)
            S.append(tmptext)
        print('test2-%d'%len(outs))
    else:
        S = []
        for _ in range(nsamples):
            out = generate(
                n_ctx=n_ctx,
                model=model,
                context=context_tokens,
                length=length,
                is_fast_pattern=fast_pattern, tokenizer=tokenizer,is_quick=quick_pattern,
                temperature=temperature, top_k=topk, top_p=topp, repitition_penalty=repetition_penalty, device=device
            )
            tmptext = untokenization(out,config,tokenizer,punc,continue_writing)
            S.append(tmptext)
    S0 = postprocess(S,raw_text,removeHighFreqWords=removeHighFreqWords,HighFreqWords=HighFreqWords)
    if len(S0)!=S:
        print(S)
        print(S0)
    return S0

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

def main(data,mode,path_config):
    ii = int(mode)
    model, tokenizer, config, device = gpt_gen.getModel(path_config=path_config)
    result = []
    if ii==1:
        r0 = gpt_gen.generating_poem('a',data, model, config, tokenizer,device,quick,num0[ii],batchGenerating=batchGenerating)
    else:
        r0 = gpt_gen.generating('a',data, model, config, tokenizer,device,quick,num0[ii],removeHighFreqWords=rmHFW[ii],HighFreqWords=HFW[ii],batchGenerating=batchGenerating)
    r0 = [rr + tags[ii] for rr in r0]
    result.extend(r0)
    print('input:%s'%data)
    print('output:\n%s'%'\n'.join(result))
    return result
if __name__=='__main__':
    mode,path_config,data = sys.argv[1:4]
    main(data,mode,path_config)