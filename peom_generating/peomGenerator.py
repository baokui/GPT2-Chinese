from gpt_gen import generating_poem,getModel
import sys
import os
import json
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
    return R
def generating(prefix,model,config,tokenizer,device,num,gpu):
    r = generating_poem(0,prefix,model,config,tokenizer,device,quick=False,num=num,batchGenerating=True,gpu=gpu,fast_pattern=True)
    return r
def fun(S,path_config,gpu,nsamples):
    model, tokenizer, config, device = getModel(path_config=path_config,gpu=gpu)
    path_target = 'data/new.txt'
    if not os.path.exists(path_target):
        os.mkdir(path_target)
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
            r = [s+'\t'+rr[len(s):] for rr in r]
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