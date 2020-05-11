from gpt_gen import *
import sys
import os
import json
def generating_poem(app,prefix,model,config,tokenizer,device,config_predict,quick=False,num=5,continue_writing=False,removeHighFreqWords=False,batchGenerating=False,gpu='0',onlyMax=False,maxNb = 20):
    if len(prefix)==0 or len(prefix)>model.config.n_ctx:
        return []
    if sum([_is_chinese_char(c) for c in prefix])<len(prefix)*0.75:
        return []
    if gpu:
        torch.cuda.set_device(int(gpu))
        device = "cuda" if torch.cuda.is_available() else "cpu"
    else:
        device = 'cpu'
    punc = '.,?!;\t 。，？！；'
    punc_end = '。；！？'
    global a
    a = app
    fast_pattern = config_predict.fast_pattern
    n_ctx = model.config.n_ctx
    length = config['length']
    nsamples = num
    #maxNb = max(nsamples,maxNb)
    maxNb = nsamples
    temperature = config['temperature']
    topk = config['topk']
    topp = config['topp']
    quick_pattern = quick
    repetition_penalty = config['repetition_penalty']
    if length == -1:
        length = model.config.n_ctx
    #raw_text = prefix[0] + prefix
    raw_text = '[MASK]' + prefix
    context_tokens = tokenizer.convert_tokens_to_ids(tokenizer.tokenize(raw_text))
    t0 = time.time()
    outs = fast_sample_sequence_batch(model, context_tokens, length, nsamples=maxNb,
                                   temperature=temperature, top_k=topk, repitition_penalty=repetition_penalty,device=device)
    S = []
    for out in outs:
        tmptext = untokenization_poem(out, tokenizer, config)
        if len(tmptext)==prefix:
            continue
        if tmptext[len(prefix)] != '，':
            continue
        idx0 = [tmptext.index(tt) for tt in punc_end]
        idx = [ii for ii in idx0 if ii!=-1]
        if len(idx)==0:
            continue
        idx1 = min(idx)
        s0 = tmptext[:idx1+1]
        tmptext1 = tmptext[idx1+1:]
        poem = poemFilter1(tmptext1,prefix,config_predict.blackwords)
        if poem:
            S.append(s0+poem)
    S = dropDuplicateContent(S)
    S = S[:nsamples]
    return S
def peomSplit(s):
    syms = '。，？；！：；“”、'
    i0 = 0
    i1 = 0
    R = []
    while i1<len(s):
        if s[i1] in syms:
            if i1>i0:
                R.append(s[i0:i1])
            i0 = i1+1
            i1 = i1+1
        else:
            i1 = i1+1
    if i1>i0:
        R.append(s[i0:i1])
    return R
def generating(prefix,model,config,tokenizer,device,num,gpu):
    r = generating_poem(0,prefix,model,config,tokenizer,device,quick=False,num=num,batchGenerating=True,gpu=gpu,fast_pattern=True)
    return r
def fun(S,path_config,gpu,nsamples):
    model, tokenizer, config, device = getModel(path_config=path_config,gpu=gpu)
    path_target = 'data/poem_white_generated.txt'
    #if not os.path.exists(path_target):
        #os.mkdir(path_target)
    N = 0
    n = 0
    for i in range(len(S)):
        if i%10==0:
            print("proceed {} poem (total {}), get {} prefix and generate {} poems".format(i,len(S),n,N))
        sents = peomSplit(S[i])
        for s in sents:
            n += 1
            if '□' in s:
                continue
            r = generating(s, model, config, tokenizer, device, nsamples, gpu)
            N+=len(r)
            if len(r)==0:
                continue
            #r = [s+rr[len(s):] for rr in r]
            with open(path_target,'a+') as f:
                f.write('\n'.join(r)+'\n')
            f.close()
def main(path_source, path_config, idx0, idx1, gpu, nsamples):
    with open(path_source, 'r') as f:
        data = json.load(f)
    S0 = data[idx0:idx1]
    batch_size=100
    i0 = 0
    i1 = i0+batch_size
    while i0<len(S0):
        print('##########################%d-%d################'%(idx0+i0,idx0+min(i1,len(S0))))
        S = S0[i0:i1]
        fun(S, path_config, gpu, nsamples)
        i0 = i1
        i1 = i1+batch_size
if __name__=='__main__':
    path_source, path_config, idx0, idx1, gpu, nsamples = sys.argv[1:]
    idx0 = int(idx0)
    idx1 = int(idx1)
    nsamples = int(nsamples)
    main(path_source, path_config, idx0, idx1, gpu, nsamples)