import re
import html
import os
import urllib.parse
from html import escape
import codecs
from datetime import datetime
from urllib.parse import unquote
import torch
import torch.nn.functional as F
from tqdm import trange
from transformers import GPT2LMHeadModel
import json
import random
from time import strftime, localtime
import time
from modules import postprocess,poemFilter1,dropDuplicateContent,_is_chinese_char,sentTriming
print_log = False
# 打印当前时间
def printTime():
    print(strftime("%Y-%m-%d %H:%M:%S", localtime()))
def is_word(word):
    for item in list(word):
        if item not in 'qwertyuiopasdfghjklzxcvbnm':
            return False
    return True

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
        # get top k
        indices_to_remove = logits < torch.topk(logits, top_k)[0][..., -1, None]
        logits[indices_to_remove] = filter_value

    if top_p > 0.0:
        #排序，获得对应index
        sorted_logits, sorted_indices = torch.sort(logits, descending=True)
        #计算累计概率
        cumulative_probs = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)

        # Remove tokens with cumulative probability above the threshold
        sorted_indices_to_remove = cumulative_probs > top_p
        # Shift the indices to the right to keep also the first token above the threshold
        #去掉累计概率大于top_p后面的item，置0
        sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
        sorted_indices_to_remove[..., 0] = 0

        #获取去掉item的index
        indices_to_remove = sorted_indices[sorted_indices_to_remove]
        #去掉
        logits[indices_to_remove] = filter_value
    return logits
def quick_sequence(model, context, length, n_ctx, tokenizer, temperature=1.0, top_k=30, top_p=0.0,
                    repitition_penalty=1.0,
                    device='cpu'):
    context = torch.tensor(context, dtype=torch.long, device=device)
    context = context.unsqueeze(0)
    generated = context
    with torch.no_grad():
        for _ in range(length):
            inputs = {'input_ids': generated[0][-(n_ctx - 1):].unsqueeze(0)}
            outputs = model(
                **inputs)  # Note: we could also use 'past' with GPT-2/Transfo-XL/XLNet (cached hidden-states)
            next_token_logits = outputs[0][0, -1, :]
            for id in set(generated):
                next_token_logits[id] /= repitition_penalty
            next_token_logits = next_token_logits / temperature
            next_token_logits[tokenizer.convert_tokens_to_ids('[UNK]')] = -float('Inf')
            #filtered_logits = top_k_top_p_filtering(next_token_logits, top_k=top_k, top_p=top_p)
            #next_token = torch.multinomial(F.softmax(filtered_logits, dim=-1), num_samples=1)
            max_token = torch.max(next_token_logits,0)
            next_token = max_token[1]
            next_token = torch.unsqueeze(next_token,0)
            next_token = torch.unsqueeze(next_token, 1)
            #print(next_token)
            #print(generated)
            generated = torch.cat((generated, next_token), dim=1)
            #print(generated)
    return generated.tolist()[0]

def sample_sequence(model, context, length, n_ctx, tokenizer, temperature=1.0, top_k=30, top_p=0.0,
                    repitition_penalty=1.0,
                    device='cpu'):
    context = torch.tensor(context, dtype=torch.long, device=device)
    context = context.unsqueeze(0)
    generated = context
    with torch.no_grad():
        for _ in range(length):
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
def sample_sequence_batch(model, context_tokens, length, n_ctx, tokenizer, nsamples,temperature=1.0, top_k=30, top_p=0.0, repitition_penalty=1.0,
                    device='cpu'):
    n = nsamples
    context = [[context_tokens]*n]
    context = torch.tensor(context, dtype=torch.long, device=device)
    context = context.squeeze(0)
    generated = context
    with torch.no_grad():
        for _ in trange(length):
            t0 = time.time()
            inputs = {'input_ids': generated[:, -(n_ctx - 1):].unsqueeze(0)}
            outputs = model(
                **inputs)  # Note: we could also use 'past' with GPT-2/Transfo-XL/XLNet (cached hidden-states)
            t1 = time.time()
            print('model predict time:%0.4f'%(t1-t0))
            next_token_logits = outputs[0][0, :, -1, :]
            '''
            for ii in range(n):
                for id in set(generated[ii]):
                    next_token_logits[ii][id] /= repitition_penalty
            '''
            next_token_logits = next_token_logits / temperature
            t2 = time.time()
            print('model temperature time:%0.4f' % (t2 - t1))
            Next = []
            for ii in range(n):
                next_token_logits[ii][tokenizer.convert_tokens_to_ids('[UNK]')] = -float('Inf')
                filtered_logits = top_k_top_p_filtering(next_token_logits[ii], top_k=top_k, top_p=top_p)
                next_token = torch.multinomial(F.softmax(filtered_logits, dim=-1), num_samples=1)
                Next.append(torch.reshape(next_token, (1, 1)))
            t3 = time.time()
            print('model top-k time:%0.4f' % (t3 - t2))
            # next_token = torch.tensor(Next)
            next_token = torch.cat(Next, dim=0)
            generated = torch.cat((generated, next_token), dim=1)
    return generated.tolist()
def sample_sequence_batch_opti(model, context_tokens, length, n_ctx, tokenizer, nsamples,temperature=1.0, top_k=30, top_p=0.0, repitition_penalty=1.0,
                    device='cpu'):
    n = nsamples
    context = [[context_tokens]*n]
    context = torch.tensor(context, dtype=torch.long, device=device)
    context = context.squeeze(0)
    generated = context
    with torch.no_grad():
        for _ in trange(length):
            t0 = time.time()
            inputs = {'input_ids': generated[:, -(n_ctx - 1):].unsqueeze(0)}
            outputs = model(
                **inputs)  # Note: we could also use 'past' with GPT-2/Transfo-XL/XLNet (cached hidden-states)
            t1 = time.time()
            print('model predict time:%0.4f'%(t1-t0))
            next_token_logits = outputs[0][0, :, -1, :]
            for ii in range(n):
                for id in set(generated[ii]):
                    next_token_logits[ii][id] /= repitition_penalty
            #for id in set(generated[ii]):
                #next_token_logits[:,id] /= repitition_penalty
            next_token_logits = next_token_logits / temperature
            t2 = time.time()
            print('model temperature time:%0.4f' % (t2 - t1))
            Next = []
            for ii in range(n):
                next_token_logits[ii][tokenizer.convert_tokens_to_ids('[UNK]')] = -float('Inf')
                filtered_logits = top_k_top_p_filtering(next_token_logits[ii], top_k=top_k, top_p=top_p)
                next_token = torch.multinomial(F.softmax(filtered_logits, dim=-1), num_samples=1)
                Next.append(torch.reshape(next_token, (1, 1)))
            t3 = time.time()
            print('model top-k time:%0.4f' % (t3 - t2))
            # next_token = torch.tensor(Next)
            next_token = torch.cat(Next, dim=0)
            generated = torch.cat((generated, next_token), dim=1)
    return generated.tolist()
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
        for i in range(length):
            #now = datetime.now()
            output = model(prev, past=past)
            #then = datetime.now()
            #a.logger.info('for : {}'.format(then - now))
            output, past = output[:2]
            output = output[-1].squeeze(0) / temperature
            filtered_logits = top_k_top_p_filtering(output, top_k=top_k, top_p=top_p)
            next_token = torch.multinomial(torch.softmax(filtered_logits, dim=-1), num_samples=1)
            generate.append(next_token.item())
            prev = next_token.view(1, 1)
    return generate
# 通过命令行参数--fast_pattern，指定模式
def generate(n_ctx, model, context, length, tokenizer,is_quick=False, temperature=1, top_k=0, top_p=0.0, repitition_penalty=1.0,
             device='cpu',
             is_fast_pattern=False):


    if is_quick:
        return quick_sequence(model, context, length, n_ctx, tokenizer=tokenizer, temperature=temperature, top_k=top_k,
                              top_p=top_p,
                              repitition_penalty=repitition_penalty, device=device)
    elif is_fast_pattern:
        return fast_sample_sequence(model, context, length, temperature=temperature, top_k=top_k, top_p=top_p,
                                    device=device)
    else:
        return sample_sequence(model, context, length, n_ctx, tokenizer=tokenizer, temperature=temperature, top_k=top_k,
                               top_p=top_p,
                               repitition_penalty=repitition_penalty, device=device)
def getModel(path_config):
    print("load model......")
    with open(path_config,'r') as f:
        config = json.load(f)
    from tokenizations import tokenization_bert
    tokenizer_path = config['tokenizer_path']
    model_path = config['model_path']
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("use device:%s"%device)
    tokenizer = tokenization_bert.BertTokenizer(vocab_file=tokenizer_path)
    model = GPT2LMHeadModel.from_pretrained(model_path)
    model.to(device)
    model.eval()
    return model,tokenizer,config,device
def untokenization(out,config,tokenizer,punc,continue_writing):
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
            text[i] = ''
        elif item == '[CLS]':
            text[i] = '\n'
        elif item == '[SEP]':
            text[i] = ''
    text = ''.join(text).replace('##', '').strip()
    # print(text)
    texts = text.split('\n')
    tmptext = texts[0]
    if continue_writing:
        if len(tmptext) < config["min_length"]:
            for ii in range(1, len(texts)):
                # tmptext += ' '
                tmptext += texts[ii]
                if len(tmptext) >= config["min_length"]:
                    break
    tmptext = tmptext.split('，')
    tmp = []
    for ii in range(len(tmptext) - 1):
        tt = tmptext[ii]
        if tt[-1] in punc:
            tmp.append(tt)
        else:
            tmp.append(tt + '，')
    tmp.append(tmptext[-1])
    tmptext = ''.join(tmp)
    return tmptext
def generating(app,prefix,model,config,tokenizer,device,config_predict,quick=False,num=5,continue_writing=False,removeHighFreqWords=False,batchGenerating=False):
    #print("start:",prefix)
    prefix0 = prefix
    if config_predict.prefixTrim:
        prefix = sentTriming(prefix0)
        if len(prefix)==0:
            prefix = prefix0
    punc = '.,?!;\t 。，？！；'
    global a
    a = app
    n_ctx = model.config.n_ctx
    fast_pattern = False
    if 'fast_pattern' in config and config['fast_pattern']=="True":
        fast_pattern = True
    length = config['length']
    nsamples = num
    temperature = config['temperature']
    topk = config['topk']
    topp = config['topp']
    quick_pattern = quick
    repetition_penalty = config['repetition_penalty']
    if length == -1:
        length = model.config.n_ctx
    raw_text = prefix
    context_tokens = tokenizer.convert_tokens_to_ids(tokenizer.tokenize(raw_text))
    if batchGenerating:
        S = []
        t0 = time.time()
        outs = sample_sequence_batch(model, context_tokens, length, n_ctx, tokenizer, nsamples, temperature=temperature,
                                     top_k=topk,
                                     top_p=topp, repitition_penalty=repetition_penalty,
                                     device=device)
        t1 = time.time()
        print('model predict all time:%0.4f' % (t1 - t0))
        for out in outs:
            tmptext = untokenization(out, config, tokenizer, punc, continue_writing)
            S.append(tmptext)
        t2 = time.time()
        print('model untokenization time:%0.4f' % (t2 - t1))
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
    if config_predict.prefixTrim:
        S = [prefix0+s[len(prefix):] for s in S]
    S = postprocess(S,prefix0,config_predict,removeHighFreqWords=removeHighFreqWords)
    S = dropDuplicateContent(S)
    t3 = time.time()
    print('text posprocess time:%0.4f' % (t3 - t2))
    return S
def generating_sentence(prefix,model,config,tokenizer):
    print("start:",prefix,config)
    n_ctx = model.config.n_ctx
    fast_pattern = False
    if config['fast_pattern']=="True":
        fast_pattern = True
    length = config['length']
    nsamples = config['nsamples']
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
        context_tokens = tokenizer.convert_tokens_to_ids(tokenizer.tokenize(raw_text))
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
                    elif item == '[CLS]':
                        text[i] = '\n\n'
                    elif item == '[SEP]':
                        text[i] = '\n'

                text = '\n'.join(text).replace('##', '').strip()
                t_no = text.split("\n")
                result = ""
                for w in t_no:
                    if result == "":
                        result = w
                    elif w != '':
                        result = result + "，" + w
                text = result
                #print(text + "。")

                S.append(text)
        if len(S) == nsamples:
            break
    return S
def nnlm_modelpredict(D_simi,D_next,config_predict,inputStr='怎么了',maxNext=3,maxChoice=10,num=5):
    output = []
    for ii in range(num+5):
        if len(output)==num:
            break
        s = inputStr
        S = []
        s0 = s
        S.append(s0)
        lastsent = s0
        for i in range(maxNext):
            if s0 in D_next:
                p = [float(tt) for tt in D_next[s0]['probs']]
                w = D_next[s0]['words']
                t = random.choices(w[:maxChoice],p[:maxChoice])[0]
                if t!=lastsent:
                    S.append(t)
                    lastsent = t
                    s0 = t
            elif s0 in D_simi:
                p = [float(tt) for tt in D_simi[s0]['probs']]
                w = D_simi[s0]['words']
                t0 = random.choices(w, p)[0]
                p = [float(tt) for tt in D_next[t0]['probs']]
                w = D_next[t0]['words']
                t = random.choices(w[:maxChoice], p[:maxChoice])[0]
                if t!=lastsent:
                    S.append(t)
                    lastsent = t
                    s0 = t
            else:
                break
        S = '，'.join(S)
        if S not in output:
            output.append(S)
        if len(output)>=num:
            break
    output = postprocess(output, inputStr,config_predict,sentEndcontent=False,removeHighFreqWords=False)
    output = dropDuplicateContent(output)
    return output
def untokenization_poem(out,tokenizer,config):
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
    if len(tmptext) < config["min_length"]:
        for ii in range(1, len(texts)):
            tmptext += '\t'
            tmptext += texts[ii]
            if len(tmptext) >= config["min_length"]:
                break
    return tmptext
def generating_poem(app,prefix,model,config,tokenizer,device,quick=False,num=5,batchGenerating=False):
    if len(prefix)>7:
        return []
    #print("start:", prefix)
    global a
    a = app
    n_ctx = model.config.n_ctx
    fast_pattern = False
    if config['fast_pattern'] == "True":
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

    #print('generating-begin for %s'%prefix)
    raw_text = prefix[0]+prefix
    context_tokens = tokenizer.convert_tokens_to_ids(tokenizer.tokenize(raw_text))
    if batchGenerating:
        outs = sample_sequence_batch(model, context_tokens, length, n_ctx, tokenizer, nsamples, temperature=temperature, top_k=topk,
                              top_p=topp, repitition_penalty=repetition_penalty,
                              device=device)
        S = []
        for out in outs:
            tmptext = untokenization_poem(out, tokenizer, config)
            poem = poemFilter1(tmptext[1:])
            if poem:
                S.append(poem)
    else:
        S = []
        for _ in range(nsamples):
            out = generate(
                n_ctx=n_ctx,
                model=model,
                context=context_tokens,
                length=length,
                is_fast_pattern=fast_pattern, tokenizer=tokenizer,
                temperature=temperature, top_k=topk, top_p=topp, repitition_penalty=repetition_penalty, device=device
            )
            tmptext = untokenization_poem(out, tokenizer, config)
            poem = poemFilter1(tmptext[1:])
            if poem:
                S.append(poem)
    S = dropDuplicateContent(S)
    return S