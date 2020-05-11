from gpt_gen import *
import sys
import os
import json
def _is_chinese_char(char):
    """Checks whether CP is the codepoint of a CJK character."""
    # This defines a "chinese character" as anything in the CJK Unicode block:
    #   https://en.wikipedia.org/wiki/CJK_Unified_Ideographs_(Unicode_block)
    #
    # Note that the CJK Unicode block is NOT all Japanese and Korean characters,
    # despite its name. The modern Korean Hangul alphabet is a different block,
    # as is Japanese Hiragana and Katakana. Those alphabets are used to write
    # space-separated words, so they are not treated specially and handled
    # like the all of the other languages.
    cp = ord(char)
    if ((cp >= 0x4E00 and cp <= 0x9FFF) or  #
            (cp >= 0x3400 and cp <= 0x4DBF) or  #
            (cp >= 0x20000 and cp <= 0x2A6DF) or  #
            (cp >= 0x2A700 and cp <= 0x2B73F) or  #
            (cp >= 0x2B740 and cp <= 0x2B81F) or  #
            (cp >= 0x2B820 and cp <= 0x2CEAF) or
            (cp >= 0xF900 and cp <= 0xFAFF) or  #
            (cp >= 0x2F800 and cp <= 0x2FA1F)):  #
        return True
    return False
def generating_poem1(app,prefix,model,config,tokenizer,device,config_predict,quick=False,num=5,continue_writing=False,removeHighFreqWords=False,batchGenerating=False,gpu='0',onlyMax=False,maxNb = 20):
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
        idx0 = [tmptext.find(tt) for tt in punc_end]
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
def generating(prefix,model,config,tokenizer,device,num,gpu,config_predict):
    r = generating_poem1(0,prefix,model,config,tokenizer,device,config_predict,quick=False,num=num,batchGenerating=True,gpu=gpu)
    return r
def fun(S,path_config,gpu,nsamples,model, tokenizer, config, device,configpredict):
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
            r = generating(s, model, config, tokenizer, device, nsamples, gpu,configpredict)
            N+=len(r)
            if len(r)==0:
                continue
            #r = [s+rr[len(s):] for rr in r]
            with open(path_target,'a+') as f:
                f.write('\n'.join(r)+'\n')
            f.close()
def main(path_source, path_config, idx0, idx1, gpu, nsamples):
    model, tokenizer, config, device = getModel(path_config=path_config, gpu=gpu)
    from Config import config_predict
    configpredict = config_predict()
    with open(path_source, 'r') as f:
        data = json.load(f)
    S0 = data[idx0:idx1]
    batch_size=100
    i0 = 0
    i1 = i0+batch_size
    while i0<len(S0):
        print('##########################%d-%d################'%(idx0+i0,idx0+min(i1,len(S0))))
        S = S0[i0:i1]
        fun(S, path_config, gpu, nsamples,model, tokenizer, config, device,configpredict)
        i0 = i1
        i1 = i1+batch_size
if __name__=='__main__':
    path_source, path_config, idx0, idx1, gpu, nsamples = sys.argv[1:]
    idx0 = int(idx0)
    idx1 = int(idx1)
    nsamples = int(nsamples)
    main(path_source, path_config, idx0, idx1, gpu, nsamples)