from gpt_gen import *
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
            self.model_configs = 'config/config_mergemodel.json'
        self.predict_nums = 5
        self.tags = '(文)'
        self.rmHFW = False
        self.repetition_penalty = 1.2
        self.temperature = 0.6
        self.length = 30
        self.resort = True
        self.style = 'prose'
def generating(prefix,model,config,tokenizer,config_predict,quick=False,num=5,continue_writing=False,removeHighFreqWords=False,gpu='0',maxNb = 10):
    black_inputs = False
    for ttt in config_predict.blackwords_inputs:
        if ttt in prefix:
            black_inputs = True
            break
    if black_inputs:
        return []
    if len(prefix)==0 or len(prefix)>25:
        return []
    if gpu:
        torch.cuda.set_device(int(gpu))
        device = "cuda" if torch.cuda.is_available() else "cpu"
    else:
        device = 'cpu'
    #if style=='prose':
        #prefix = prefix[0] + prefix
    prefix0 = prefix
    if config_predict.prefixTrim:
        prefix = sentTriming(prefix0)
        if len(prefix)==0:
            prefix = prefix0
    punc = '.,?!;\t 。，？！；'
    fast_pattern = config_predict.fast_pattern
    n_ctx = model.config.n_ctx
    len_prefix = len(prefix)
    if len_prefix < 5:
        max_genlen = 20
    elif len_prefix < 10:
        max_genlen = 25
    else:
        max_genlen = config['length']
    length = min(max_genlen,n_ctx-len_prefix-3)
    nsamples = num
    maxNb = max(nsamples,maxNb)
    temperature = config['temperature']
    topk = config['topk']
    topp = config['topp']
    quick_pattern = quick
    repetition_penalty = config['repetition_penalty']
    if length == -1:
        length = model.config.n_ctx
    raw_text = prefix
    S0 = []
    for token in ['[MASK_gou]','[MASK_prose]']:
        S = []
        id_msk = tokenizer.convert_tokens_to_ids(token)
        context_tokens = [id_msk] + tokenizer.convert_tokens_to_ids(tokenizer.tokenize(raw_text))
        outs = fast_sample_sequence_batch(model, context_tokens, length, nsamples=maxNb,
                                          temperature=temperature, top_k=topk, repitition_penalty=repetition_penalty,
                                          device=device)
        for out in outs:
            tmptext = untokenization(out[1:], config, tokenizer, punc, continue_writing)
            S.append(tmptext)
        if config_predict.prefixTrim:
            S = [prefix0+s[len(prefix):] for s in S]
        S = postprocess(S,prefix0,config_predict,removeHighFreqWords=removeHighFreqWords)
        S = dropDuplicateContent(S)
        if config_predict.resort:
            if len(S)>0:
                S = resort(prefix0, S, config_predict)
        S = S[:nsamples]
        S0.extend([s+'('+token+')' for s in S])
    #if style == 'prose':
        #S = [r[1:] for r in S]
    return S0
def main():
    ConfigPredict = config_predict(model_config='config/config_mergemodel.json')
    path_configs = ConfigPredict.model_configs
    gpu = '0'
    model, tokenizer, config, device = getModel(path_config=path_configs, gpu=gpu)
    data = '我们'
    result = generating(data, model, config, tokenizer, ConfigPredict)
