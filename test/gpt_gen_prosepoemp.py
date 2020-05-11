from gpt_gen import *
from Config import Config
import sys
class config_predict_prosepoem(Config):
    # 定义构造方法
    def __init__(self, model_config='', gpus=''):  # __init__() 是类的初始化方法；它在类的实例化操作后 会自动调用，不需要手动调用；
        super().__init__()
        if gpus:
            self.gpus = gpus
        else:self.gpus = '0'
        if model_config:
            self.model_configs = model_config
        else:
            self.model_configs = 'demo_config/config_prosepoem_pre.json'
            #self.model_configs = '../bin/config/config_godText_large1.json'
        self.predict_nums = 5
        self.tags = ''
        self.rmHFW = False
        self.repetition_penalty = 1.2
        self.temperature = 0.6
        self.length = 30
        self.resort = True
        self.style = 'prose'
def untokenization(out,config,tokenizer,punc,continue_writing):
    text = tokenizer.convert_ids_to_tokens(out)
    for i, item in enumerate(text[:-1]):  # 确保英文前后有空格
        if is_word(item) and is_word(text[i + 1]):
            text[i] = item + ' '
    tmptext = ''
    for i, item in enumerate(text):
        if item == '[MASK]':
            text[i] = ''
        elif item == '[PAD]':
            text[i] = ''
        elif item == '[UNK]':
            text[i] = ''
        elif item == '[CLS]':
            text[i] = '\n'
        elif item == '[SEP]':
            text[i] = '\n'
        tmptext+=text[i]
    return tmptext
def generating(prefix,model,config,tokenizer,config_predict,max_genlen = 1000,quick=False,num=5,continue_writing=False,removeHighFreqWords=False,batchGenerating=False,gpu='0',onlyMax=False,maxNb = 20):
    if gpu:
        torch.cuda.set_device(int(gpu))
        device = "cuda" if torch.cuda.is_available() else "cpu"
    else:
        device = 'cpu'
    #if style=='prose':
        #prefix = prefix[0] + prefix
    prefix0 = prefix
    if config_predict.prefixTrim:
        if len(prefix)==0:
            prefix = prefix0
        else:
            prefix = sentTriming(prefix0)
    punc = '.,?!;\t 。，？！；'
    fast_pattern = config_predict.fast_pattern
    n_ctx = model.config.n_ctx
    len_prefix = len(prefix)
    length = min(max_genlen,n_ctx-len_prefix-1)
    nsamples = num
    maxNb = max(nsamples,maxNb)
    temperature = config['temperature']
    topk = config['topk']
    topp = config['topp']
    quick_pattern = quick
    repetition_penalty = config['repetition_penalty']
    if length == -1:
        length = model.config.n_ctx
    raw_text = '[MASK]'+prefix
    context_tokens = tokenizer.convert_tokens_to_ids(tokenizer.tokenize(raw_text))
    outs = fast_sample_sequence_batch(model, context_tokens, length, nsamples=maxNb,
                                           temperature=temperature, top_k=topk, repitition_penalty=repetition_penalty,device=device)
    S = []
    for out in outs:
        tmptext = untokenization(out, config, tokenizer, punc, continue_writing)
        S.append(tmptext)
    if config_predict.prefixTrim:
        S = [prefix0+s[len(prefix):] for s in S]
    return S
def main(path_source,path_target):
    config_predict = config_predict_prosepoem()
    model,tokenizer,config,device = getModel(config_predict.model_configs, gpu=config_predict.gpus)
    with open(path_source,'r') as f:
        Data = f.read().strip().split('\n')
    num = 10
    max_genlen = 1024
    S = []
    for data in Data:
        T = generating(data,model,config,tokenizer,config_predict,num=num,max_genlen=max_genlen)
        T = [data+'--\n'+t+'\n' for t in T]
        S.extend(T)
        with open(path_target,'w') as f:
            f.write('\n'.join(S))
if __name__=='__main__':
    path_source, path_target = sys.argv[1:3]
    main(path_source,path_target)