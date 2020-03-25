import torch
import torch.nn.functional as F
from tqdm import trange
from transformers import GPT2LMHeadModel
import json
import jieba
import sys
def tokenizer_seg(words,path_words='../model/model_dabaigou_seg/vocab.txt'):
    with open(path_words,'r') as f:
        v = f.read().strip().split('\n')
    token_unk = v.index('[UNK]')
    r = []
    for w in words:
        if w not in v:
            r.append(token_unk)
        else:
            r.append(v.index(w))
    return r
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False
def url_parse(urlstr):
    modelidex,inputStr,nsamples = 0,'祝你',3
    D = {}
    if '?' in urlstr:
        s0 = urlstr[urlstr.find('?')+1:]
        T = s0.split('&')
        for t in T:
            tt = t.split('=')
            D[tt[0]] = tt[1]
    print('url:%s'%urlstr)
    print('result:')
    print(D)
    if 'model' in D:
        if is_number(D['model']):
            modelidex = int(float(D['model']))
    if 'inputStr' in D:
        inputStr = D['inputStr']
    if 'nsamples' in D:
        if is_number(D['nsamples']):
            nsamples = int(float(D['nsamples']))
    return modelidex,inputStr,nsamples
def url_parse1(urlstr):
    modelidex, inputStr, nsamples = 0, '祝你', 3
    D = {}
    if '?' in urlstr:
        s0 = urlstr[urlstr.find('?') + 1:]
        T = s0.split('&')
        for t in T:
            tt = t.split('=')
            D[tt[0]] = tt[1]
    print('url:%s' % urlstr)
    print('result:')
    print(D)
    modelidex = int(float(D['model']))
    inputStr = D['inputStr']
    nsamples = int(float(D['nsamples']))
    return modelidex,inputStr,nsamples
def is_word(word):
    for item in list(word):
        if item not in 'qwertyuiopasdfghjklzxcvbnm':
            return False
    return True
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
def top_k_top_p_filtering(logits, top_k=0, top_p=0.0, filter_value=-float('Inf')):
    """ Filter a distribution of logits using top-k and/or nucleus (top-p) filtering
        Args:
            logits: logits distribution shape (vocabulary size)
            top_k > 0: keep only top k tokens with highest probability (top-k filtering).
            top_p > 0.0: keep the top tokens with cumulative probability >= top_p (nucleus filtering).
                Nucleus filtering is described in Holtzman et al. (http://arxiv.org/abs/1904.09751)
        From: https://gist.github.com/thomwolf/1a5a29f6962089e871b94cbd09daf317
    """
    assert logits.dim() == 1  # batch size 1 for now - could be updated for more but the code would be less clear
    top_k = min(top_k, logits.size(-1))  # Safety check
    if top_k > 0:
        # Remove all tokens with a probability less than the last token of the top-k
        indices_to_remove = logits < torch.topk(logits, top_k)[0][..., -1, None]
        logits[indices_to_remove] = filter_value

    if top_p > 0.0:
        sorted_logits, sorted_indices = torch.sort(logits, descending=True)
        cumulative_probs = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)

        # Remove tokens with cumulative probability above the threshold
        sorted_indices_to_remove = cumulative_probs > top_p
        # Shift the indices to the right to keep also the first token above the threshold
        sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
        sorted_indices_to_remove[..., 0] = 0

        indices_to_remove = sorted_indices[sorted_indices_to_remove]
        logits[indices_to_remove] = filter_value
    return logits
def sample_sequence(model, context, length, n_ctx, tokenizer, temperature=1.0, top_k=30, top_p=0.0,
                    repitition_penalty=1.0,
                    device='cpu'):
    context = torch.tensor(context, dtype=torch.long, device=device)
    context = context.unsqueeze(0)
    generated = context
    with torch.no_grad():
        for _ in trange(length):
            inputs = {'input_ids': generated[0][-(n_ctx - 1):].unsqueeze(0)}
            outputs = model(
                **inputs)  # Note: we could also use 'past' with GPT-2/Transfo-XL/XLNet (cached hidden-states)
            next_token_logits = outputs[0][0, -1, :]
            for id in set(generated):
                next_token_logits[id] /= repitition_penalty
            next_token_logits = next_token_logits / temperature
            next_token_logits[tokenizer.convert_tokens_to_ids('[UNK]')] = -float('Inf')
            filtered_logits = top_k_top_p_filtering(next_token_logits, top_k=top_k, top_p=top_p)
            next_token = torch.multinomial(F.softmax(filtered_logits, dim=-1), num_samples=1)
            generated = torch.cat((generated, next_token.unsqueeze(0)), dim=1)
    return generated.tolist()[0]
def fast_sample_sequence(model, context, length, temperature=1.0, top_k=30, top_p=0.0, device='cpu'):
    inputs = torch.LongTensor(context).view(1, -1).to(device)
    if len(context) > 1:
        _, past = model(inputs[:, :-1], None)[:2]
        prev = inputs[:, -1].view(1, -1)
    else:
        past = None
        prev = inputs
    generate = [] + context
    with torch.no_grad():
        for i in trange(length):
            output = model(prev, past=past)
            output, past = output[:2]
            output = output[-1].squeeze(0) / temperature
            filtered_logits = top_k_top_p_filtering(output, top_k=top_k, top_p=top_p)
            next_token = torch.multinomial(torch.softmax(filtered_logits, dim=-1), num_samples=1)
            generate.append(next_token.item())
            prev = next_token.view(1, 1)
    return generate
# 通过命令行参数--fast_pattern，指定模式
def generate(n_ctx, model, context, length, tokenizer, temperature=1, top_k=0, top_p=0.0, repitition_penalty=1.0,
             device='cpu',
             is_fast_pattern=False):
    if is_fast_pattern:
        return fast_sample_sequence(model, context, length, temperature=temperature, top_k=top_k, top_p=top_p,
                                    device=device)
    else:
        return sample_sequence(model, context, length, n_ctx, tokenizer=tokenizer, temperature=temperature, top_k=top_k,
                               top_p=top_p,
                               repitition_penalty=repitition_penalty, device=device)
def getModel(path_config):
    with open(path_config,'r') as f:
        config = json.load(f)
    from tokenizations import tokenization_bert
    tokenizer_path = config['tokenizer_path']
    model_path = config['model_path']
    device = 'cpu'
    tokenizer = tokenization_bert.BertTokenizer(vocab_file=tokenizer_path)
    model = GPT2LMHeadModel.from_pretrained(model_path)
    model.to(device)
    model.eval()
    return model,tokenizer,config
def generating(prefix,model,config,tokenizer,segment=False,nsamples=10,modelType='other'):
    if modelType=='poem':
        prefix = prefix[0]+prefix
    n_ctx = model.config.n_ctx
    fast_pattern = True
    length = min(config['length'],n_ctx-len(prefix))
    #nsamples = config['nsamples']
    batch_size = config['batch_size']
    temperature = config['temperature']
    topk = config['topk']
    topp = config['topp']
    repetition_penalty = config['repetition_penalty']
    device = 'cpu'
    if length == -1:
        length = model.config.n_ctx
    S = []
    print('generating-begin for %s'%prefix)
    while True:
        raw_text = prefix
        print(raw_text)
        if segment:
            context_tokens = tokenizer_seg(list(jieba.cut(raw_text)))
        else:
            context_tokens = tokenizer.convert_tokens_to_ids(tokenizer.tokenize(raw_text))
        print(context_tokens)
        generated = 0
        print(n_ctx, context_tokens, length, fast_pattern, temperature, topk, topp, repetition_penalty, device)
        for _ in range(nsamples // batch_size):
            out = generate(
                n_ctx=n_ctx,
                model=model,
                context=context_tokens,
                length=length,
                is_fast_pattern=fast_pattern, tokenizer=tokenizer,
                temperature=temperature, top_k=topk, top_p=topp, repitition_penalty=repetition_penalty, device=device
            )
            for i in range(batch_size):
                generated += 1
                text = tokenizer.convert_ids_to_tokens(out)
                for i, item in enumerate(text[:-1]):  # 确保英文前后有空格
                    if is_word(item) and is_word(text[i + 1]):
                        text[i] = item + ' '
                for i, item in enumerate(text):
                    if item == '[MASK]':
                        text[i] = ''
                    elif item == '[PAD]':
                        text[i] = ''
                    elif item == '[UNK]':
                        text[i] = ' '
                    elif item == '[CLS]':
                        text[i] = '\n\n'
                    elif item == '[SEP]':
                        text[i] = '\n'
                text = ''.join(text).replace('##', '').strip()
                # print(text)
                texts = text.split('\n')
                tmptext = texts[0]
                if len(tmptext)<config["min_length"]:
                    for ii in range(1,len(texts)):
                        tmptext += '\t'
                        tmptext += texts[ii]
                        if len(tmptext)>=config["min_length"]:
                            break
                if modelType=='poem':
                    tmptext = tmptext[1:]
                S.append(tmptext)
        if len(S) == nsamples:
            break
    return S
def generating_head(prefix,model,config,tokenizer,segment=False,nsamples=10):
    sep = '，。？'
    S = []
    def getHead(Str):
        ii = 0
        for ii in range(len(Str)):
            if Str[ii] in sep:
                break
        return Str[:ii+1]
    for i in range(nsamples):
        p = prefix[0]
        inputStr = ''
        for j in range(len(prefix)):
            inputStr = inputStr + getHead(p[len(inputStr):]) + prefix[j]
            p = generating(inputStr,model,config,tokenizer,segment=False,nsamples=1,modelType='poem')[0]
            #print('input:%s'%inputStr)
            #print('output:%s'%p)
        S.append(p)
    return S
def main(path_config,mode,path_source,path_target,modelType):
    model, tokenizer, config = getModel(path_config=path_config)
    if mode=='seg':
        segment=True
    else:
        segment = False
    with open(path_source,'r') as f:
        lines = f.read().strip().split('\n')
    S = []
    for i in range(len(lines)):
        inputStr = lines[i].strip().lower()
        if modelType=='poem_head':
            result = generating_head(inputStr, model, config, tokenizer, segment)
        else:
            result = generating(inputStr, model, config, tokenizer, segment,modelType=modelType)
        d = {}
        d['inputStr'] = inputStr
        d['generatingStr'] = result
        print('processing %d(total %d)'%(i,len(lines)))
        print(d)
        S.append(d)
        if len(S)%10==0:
            with open(path_target,'w') as f:
                json.dump(S,f,ensure_ascii=False,indent=4)
    with open(path_target, 'w') as f:
        json.dump(S, f, ensure_ascii=False, indent=4)
if __name__=='__main__':
    path_config,mode,path_source,path_target = sys.argv[1:5]
    modelType = sys.argv[-1]
    main(path_config,mode,path_source,path_target,modelType)