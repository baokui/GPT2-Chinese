from gpt_gen import generating_poem,getModel
import sys
import os
import json
def peomSplit(s):
    syms = '。，？；！'
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
    r = generating_poem(prefix,model,config,tokenizer,device,quick=False,num=num,batchGenerating=True,gpu=gpu)
    return r
def main(path_source,path_config,idx0,idx1,gpu,nsamples):
    model, tokenizer, config, device = getModel(path_config=path_config,gpu=gpu)
    with open(path_source,'r') as f:
        data = json.load(f)
    path_target = 'data/'+str(idx0)+'_'+str(idx1)
    if not os.path.exists(path_target):
        os.mkdir(path_target)
    D_prefix = {}
    S = data[idx0:idx1]
    R = {}
    for i in range(len(S)):
        if i%2==0:
            n = sum([len(R[tt]) for tt in R])
            print("proceed {} poem (total {}), get {} files and generate {} poems".format(i,len(S),len(D_prefix),n))
        sents = peomSplit(S[i])
        for s in sents:
            r = generating(s, model, config, tokenizer, device, nsamples, gpu)
            r = [s+'\t'+rr[len(s):] for rr in r]
            if s[0] in D_prefix:
                D_prefix[s[0]]+=1
                R[s[0]].extend(r)
            else:
                D_prefix[s[0]] = 1
                R[s[0]] = r
            if D_prefix[s[0]]%10==0:
                with open(path_target+'/'+s[0]+'.json','w') as f:
                    json.dump(R[s[0]],f,ensure_ascii=False,indent=4)
    for s in D_prefix:
        with open(path_target + '/' + s + '.json', 'w') as f:
            json.dump(R[s], f, ensure_ascii=False, indent=4)
if __name__=='__main__':
    path_source, path_config, idx0, idx1, gpu, nsamples = sys.argv[1:]
    idx0 = int(idx0)
    idx1 = int(idx1)
    nsamples = int(nsamples)
    main(path_source, path_config, idx0, idx1, gpu, nsamples)