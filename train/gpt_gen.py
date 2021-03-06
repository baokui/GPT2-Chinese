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
from modules import postprocess,poemFilter1,dropDuplicateContent,_is_chinese_char,sentTriming,findMaxMatch,resort
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
    #assert logits.dim() == 1  # batch size 1 for now - could be updated for more but the code would be less clear
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
    idx_unk = tokenizer.convert_tokens_to_ids('[UNK]')
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
            next_token_logits = outputs[0][0, :, -1, :]
            for ii in range(n):
                for id in set(generated[ii]):
                    next_token_logits[ii][id] /= repitition_penalty
            next_token_logits = next_token_logits / temperature
            Next = []
            for ii in range(n):
                next_token_logits[ii][tokenizer.convert_tokens_to_ids('[UNK]')] = -float('Inf')
                filtered_logits = top_k_top_p_filtering(next_token_logits[ii], top_k=top_k, top_p=top_p)
                next_token = torch.multinomial(F.softmax(filtered_logits, dim=-1), num_samples=1)
                Next.append(torch.reshape(next_token, (1, 1)))
            # next_token = torch.tensor(Next)
            next_token = torch.cat(Next, dim=0)
            generated = torch.cat((generated, next_token), dim=1)
    return generated.tolist()
def sample_sequence_batch_opti(model, context_tokens, length, n_ctx, tokenizer, nsamples,temperature=1.0, top_k=30, top_p=0.0, repitition_penalty=1.0,
                    device='cpu'):
    idx_unk = tokenizer.convert_tokens_to_ids('[UNK]')
    n = nsamples
    context = [[context_tokens]*n]
    context = torch.tensor(context, dtype=torch.long, device=device)
    context = context.squeeze(0)
    generated = context
    if repitition_penalty!=1.0:
        set_generated = [list(context[0].cpu().numpy()) for _ in range(n)]
        T0 = 0
        T1 = 0
        T2 = 0
        T3 = 0
        rev_repitition_penalty = 1.0/repitition_penalty
        rev_temperature = 1.0/temperature
        A0 = []
        A1 = []
        for kk in range(len(set_generated)):
            for jj in range(len(set_generated[kk])):
                A0.append(kk)
                A1.append(set_generated[kk][jj])
        with torch.no_grad():
            for _ in range(length):
                t0 = time.time()
                inputs = {'input_ids': generated[:, -(n_ctx - 1):].unsqueeze(0)}
                outputs = model(
                    **inputs)  # Note: we could also use 'past' with GPT-2/Transfo-XL/XLNet (cached hidden-states)
                t1 = time.time()
                next_token_logits = outputs[0][0, :, -1, :]
                next_token_logits[A0,A1] *= rev_repitition_penalty
                next_token_logits = next_token_logits * rev_temperature
                t2 = time.time()
                next_token_logits[:, idx_unk] = -float('Inf')
                filtered_logits = top_k_top_p_filtering(next_token_logits, top_k=top_k, top_p=0)
                next_token = torch.multinomial(F.softmax(filtered_logits, dim=-1), num_samples=1)
                t3 = time.time()
                NT_np = next_token.cpu().numpy()[:, 0]
                for ii in range(n):
                    #if next_token[ii] not in set_generated[ii]:
                    #set_generated[ii].append(next_token[ii])
                    A0.append(ii)
                    A1.append(NT_np[ii])
                t4 = time.time()
                T0 = T0 + t1 - t0
                T1 = T1 + t2 - t1
                T2 = T2 + t3 - t2
                T3 = T3 + t4 - t3
                generated = torch.cat((generated, next_token), dim=1)
            #print("predict:penalty:topk:update-%0.4f:%0.4f:%0.4f:%0.4f"%(T0,T1,T2,T3))
            #print(TT0,TT1,TT2,TT3,TT4)
            return generated.tolist()
    else:
        T0 = 0
        T1 = 0
        T2 = 0
        with torch.no_grad():
            for _ in trange(length):
                t0 = time.time()
                inputs = {'input_ids': generated[:, -(n_ctx - 1):].unsqueeze(0)}
                outputs = model(
                    **inputs)  # Note: we could also use 'past' with GPT-2/Transfo-XL/XLNet (cached hidden-states)
                t1 = time.time()
                T0 = T0+t1-t0
                next_token_logits = outputs[0][0, :, -1, :]
                next_token_logits = next_token_logits / temperature
                t2 = time.time()
                T1 = T1+t2-t1
                Next = []
                for ii in range(n):
                    tt0 = time.time()
                    next_token_logits[ii][tokenizer.convert_tokens_to_ids('[UNK]')] = -float('Inf')
                    tt1 = time.time()
                    filtered_logits = top_k_top_p_filtering(next_token_logits[ii], top_k=top_k, top_p=top_p)
                    tt2 = time.time()
                    next_token = torch.multinomial(F.softmax(filtered_logits, dim=-1), num_samples=1)
                    tt3 = time.time()
                    Next.append(torch.reshape(next_token, (1, 1)))
                    #set_generated[ii].update(next_token)
                t3 = time.time()
                T2 = T2+t3-t2
                # next_token = torch.tensor(Next)
                next_token = torch.cat(Next, dim=0)
                generated = torch.cat((generated, next_token), dim=1)
            #print(T0,T1,T2)
            return generated.tolist()
def sample_sequence_batch_max(model, context_tokens, length, n_ctx, tokenizer, nsamples,temperature=1.0, top_k=30, top_p=0.0, repitition_penalty=1.0,
                    device='cpu'):
    idx_unk = tokenizer.convert_tokens_to_ids('[UNK]')
    n = nsamples
    context = [[context_tokens]*n]
    context = torch.tensor(context, dtype=torch.long, device=device)
    context = context.squeeze(0)
    generated = context
    if repitition_penalty!=1.0:
        set_generated = [list(context[0]) for _ in range(n)]
        T0 = 0
        T1 = 0
        T2 = 0
        TT0,TT1,TT2,TT3,TT4=0,0,0,0,0
        rev_repitition_penalty = 1.0/repitition_penalty
        rev_temperature = 1.0/temperature
        A0 = []
        A1 = []
        for kk in range(len(set_generated)):
            for jj in range(len(set_generated[kk])):
                A0.append(kk)
                A1.append(set_generated[kk][jj])
        with torch.no_grad():
            for _ in range(length):
                t0 = time.time()
                inputs = {'input_ids': generated[:, -(n_ctx - 1):].unsqueeze(0)}
                outputs = model(
                    **inputs)  # Note: we could also use 'past' with GPT-2/Transfo-XL/XLNet (cached hidden-states)
                t1 = time.time()
                T0 = T0+t1-t0
                next_token_logits = outputs[0][0, :, -1, :]
                #for ii in range(n):
                    #for id in set(generated[ii]):
                        #A.append([ii,id])
                        #next_token_logits[ii][id] *= rev_repitition_penalty
                next_token_logits[A0,A1] *= rev_repitition_penalty
                next_token_logits = next_token_logits * rev_temperature
                t2 = time.time()
                T1 = T1+t2-t1
                '''
                Next = []
                for ii in range(n):
                    tt0 = time.time()
                    next_token_logits[ii][tokenizer.convert_tokens_to_ids('[UNK]')] = -float('Inf')
                    tt1 = time.time()
                    filtered_logits = top_k_top_p_filtering(next_token_logits[ii], top_k=top_k, top_p=top_p)
                    tt2 = time.time()
                    next_token = torch.multinomial(F.softmax(filtered_logits, dim=-1), num_samples=1)
                    tt3 = time.time()
                    Next.append(torch.reshape(next_token, (1, 1)))
                    tt4 = time.time()
                    if next_token not in set_generated[ii]:
                        set_generated[ii].append(next_token)
                        A0.append(ii)
                        A1.append(next_token)
                    tt5 = time.time()
                    TT0 = tt1-tt0+TT0
                    TT1 = tt2-tt1+TT1
                    TT2 = tt3-tt2+TT2
                    TT3 = tt4-tt3+TT3
                    TT4 = tt5-tt4+TT4
                    #set_generated[ii].update(next_token)
                t3 = time.time()
                T2 = T2+t3-t2
                # next_token = torch.tensor(Next)
                next_token = torch.cat(Next, dim=0)
                '''
                next_token_logits[:, idx_unk] = -float('Inf')
                #filtered_logits = top_k_top_p_filtering(next_token_logits, top_k=top_k, top_p=0)
                #next_token = torch.multinomial(F.softmax(filtered_logits, dim=-1), num_samples=1)
                next_token = torch.argmax(next_token_logits, dim=-1, keepdim=True)
                for ii in range(len(set_generated)):
                    if next_token[ii] not in set_generated[ii]:
                        set_generated[ii].append(next_token[ii])
                        A0.append(ii)
                        A1.append(next_token[ii])
                generated = torch.cat((generated, next_token), dim=1)
            #print(T0,T1,T2)
            #print(TT0,TT1,TT2,TT3,TT4)
            return generated.tolist()
    else:
        T0 = 0
        T1 = 0
        T2 = 0
        with torch.no_grad():
            for _ in trange(length):
                t0 = time.time()
                inputs = {'input_ids': generated[:, -(n_ctx - 1):].unsqueeze(0)}
                outputs = model(
                    **inputs)  # Note: we could also use 'past' with GPT-2/Transfo-XL/XLNet (cached hidden-states)
                t1 = time.time()
                T0 = T0+t1-t0
                next_token_logits = outputs[0][0, :, -1, :]
                next_token_logits = next_token_logits / temperature
                t2 = time.time()
                T1 = T1+t2-t1
                Next = []
                for ii in range(n):
                    tt0 = time.time()
                    next_token_logits[ii][tokenizer.convert_tokens_to_ids('[UNK]')] = -float('Inf')
                    tt1 = time.time()
                    filtered_logits = top_k_top_p_filtering(next_token_logits[ii], top_k=top_k, top_p=top_p)
                    tt2 = time.time()
                    next_token = torch.multinomial(F.softmax(filtered_logits, dim=-1), num_samples=1)
                    tt3 = time.time()
                    Next.append(torch.reshape(next_token, (1, 1)))
                    #set_generated[ii].update(next_token)
                t3 = time.time()
                T2 = T2+t3-t2
                # next_token = torch.tensor(Next)
                next_token = torch.cat(Next, dim=0)
                generated = torch.cat((generated, next_token), dim=1)
            #print(T0,T1,T2)
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
def fast_sample_sequence_batch(model, context, length, nsamples=10,temperature=1.0, top_k=30, repitition_penalty=1.0, device='cpu'):
    #inputs = torch.LongTensor(context).view(1, -1).to(device)
    rev_repitition_penalty = 1.0 / repitition_penalty
    inputs = [context] * nsamples
    inputs = torch.tensor(inputs, dtype=torch.long, device=device)
    if len(context) > 1:
        _, past = model(inputs[:, :-1], None)[:2]
        #prev = inputs[:, -1].view(1, -1)
        prev = inputs[:, -1].view(-1, 1)
    else:
        past = None
        prev = inputs
    generate = [[t for t in context] for _ in range(nsamples)]
    A0 = []
    A1 = []
    for kk in range(len(generate)):
        for jj in range(len(generate[kk])):
            A0.append(kk)
            A1.append(generate[kk][jj])
    with torch.no_grad():
        for i in range(length):
            #now = datetime.now()
            output = model(prev, past=past)
            #then = datetime.now()
            #a.logger.info('for : {}'.format(then - now))
            output, past = output[:2]
            #output = output[-1].squeeze(0) / temperature
            output = output.squeeze(1)
            output[A0, A1] *= rev_repitition_penalty
            output /= temperature
            filtered_logits = top_k_top_p_filtering(output, top_k=top_k, top_p=0)
            next_token = torch.multinomial(torch.softmax(filtered_logits, dim=-1), num_samples=1)
            #generate.append(next_token.item())
            #prev = next_token.view(1, 1)
            prev = next_token
            NT_np = next_token.cpu().numpy()
            for ii in range(nsamples):
                generate[ii].append(NT_np[ii][0])
                A0.append(ii)
                A1.append(NT_np[ii])
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
def getModel(path_config,gpu='0'):
    print("load model......")
    if gpu:
        torch.cuda.set_device(int(gpu))
        device = "cuda" if torch.cuda.is_available() else "cpu"
    else:
        device = 'cpu'
    print("use device:%s" % device)
    #os.environ["CUDA_VISIBLE_DEVICES"] = gpu
    with open(path_config,'r') as f:
        config = json.load(f)
    from tokenizations import tokenization_bert
    tokenizer_path = config['tokenizer_path']
    model_path = config['model_path']


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
        if len(tt)>0:
            if tt[-1] in punc:
                tmp.append(tt)
            else:
                tmp.append(tt + '，')
    tmp.append(tmptext[-1])
    tmptext = ''.join(tmp)
    return tmptext
def generating_poem(app,prefix,model,config,tokenizer,device,config_predict,quick=False,num=5,continue_writing=False,removeHighFreqWords=False,batchGenerating=False,gpu='0',onlyMax=False,maxNb = 20):
    black_inputs = False
    for ttt in config_predict.blackwords_inputs:
        if ttt in prefix:
            black_inputs = True
            break
    if black_inputs:
        return [],''
    if len(prefix)==0 or len(prefix)>10:
        return [],''
    if sum([_is_chinese_char(c) for c in prefix])<len(prefix)*0.75:
        return [],''
    if gpu:
        torch.cuda.set_device(int(gpu))
        device = "cuda" if torch.cuda.is_available() else "cpu"
    else:
        device = 'cpu'
    punc = '.,?!;\t 。，？！；'
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
    raw_text = prefix
    id_msk = tokenizer.convert_tokens_to_ids('[MASK]')
    context_tokens = [id_msk]+tokenizer.convert_tokens_to_ids(tokenizer.tokenize(raw_text))
    S = []
    err = ''
    try:
        outs = fast_sample_sequence_batch(model, context_tokens, length, nsamples=maxNb,
                                           temperature=temperature, top_k=topk, repitition_penalty=repetition_penalty,device=device)
        for out in outs:
            tmptext = untokenization_poem(out, tokenizer, config)
            poem = poemFilter1(tmptext,prefix,config_predict.blackwords)
            if poem:
                S.append(poem)
        S = dropDuplicateContent(S)
        S = S[:nsamples]
    except Exception as e:
        err = str(e)
    return S,err
def generating(app,prefix,model,config,tokenizer,device,config_predict,quick=False,num=5,continue_writing=False,removeHighFreqWords=False,batchGenerating=False,gpu='0',onlyMax=False,maxNb = 10,style=''):
    #print("start:",prefix)
    #os.environ["CUDA_VISIBLE_DEVICES"] = gpu
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
    global a
    a = app
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
    id_msk = tokenizer.convert_tokens_to_ids('[MASK]')
    context_tokens = [id_msk] + tokenizer.convert_tokens_to_ids(tokenizer.tokenize(raw_text))
    if batchGenerating:
        S = []
        if onlyMax:
            outs = sample_sequence_batch_max(model, context_tokens, length, n_ctx, tokenizer, nsamples=2,
                                              temperature=temperature,
                                              top_k=topk,
                                              top_p=topp, repitition_penalty=repetition_penalty,
                                              device=device)
        else:
            if fast_pattern:
                outs = fast_sample_sequence_batch(model, context_tokens, length, nsamples=maxNb,
                                           temperature=temperature, top_k=topk, repitition_penalty=repetition_penalty,device=device)
            else:
                outs = sample_sequence_batch_opti(model, context_tokens, length, n_ctx, tokenizer, maxNb, temperature=temperature,
                                         top_k=topk,
                                         top_p=topp, repitition_penalty=repetition_penalty,
                                         device=device)
        for out in outs:
            tmptext = untokenization(out, config, tokenizer, punc, continue_writing)
            S.append(tmptext)
    else:
        S = []
        for _ in range(maxNb):
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
    if config_predict.resort:
        if len(S)>0:
            S = resort(prefix0, S, config_predict)
    S = S[:nsamples]
    #if style == 'prose':
        #S = [r[1:] for r in S]
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
    prefix,punc = findMaxMatch(inputStr,D_simi,D_next,config_predict)
    if punc=='':
        punc = '，'
    if len(prefix)==0:
        return []
    output = []
    for ii in range(num+5):
        if len(output)==num:
            break
        s0 = prefix
        S = []
        #S.append(inputStr)
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
        S = inputStr+punc+'，'.join(S)
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
def generating_poem0(app,prefix,model,config,tokenizer,device,quick=False,num=5,batchGenerating=False,gpu='0',onlyMax=False,fast_pattern=False):
    if gpu:
        torch.cuda.set_device(int(gpu))
        device = "cuda" if torch.cuda.is_available() else "cpu"
    else:
        device = 'cpu'
    #print("use device:%s" % device)
    if len(prefix)>10:
        return []
    #print("start:", prefix)
    global a
    a = app
    n_ctx = model.config.n_ctx
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
        if onlyMax:
            outs = sample_sequence_batch_max(model, context_tokens, length, n_ctx, tokenizer, nsamples=2,
                                              temperature=temperature, top_k=topk,
                                              top_p=topp, repitition_penalty=repetition_penalty,
                                              device=device)
        else:
            if fast_pattern:
                outs = fast_sample_sequence_batch(model, context_tokens, length, nsamples=nsamples,
                                                  temperature=temperature, top_k=topk,
                                                  repitition_penalty=repetition_penalty, device=device)
            else:
                outs = sample_sequence_batch_opti(model, context_tokens, length, n_ctx, tokenizer, nsamples, temperature=temperature, top_k=topk,
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
def testFun(app,prefix,model,config,tokenizer,device,config_predict,quick=False,num=5,continue_writing=False,removeHighFreqWords=False,batchGenerating=False,gpu='0',onlyMax=False,maxNb = 20):
    #print("start:",prefix)
    #os.environ["CUDA_VISIBLE_DEVICES"] = gpu
    if len(prefix)==0 or len(prefix)>model.config.n_ctx:
        return []
    if gpu:
        torch.cuda.set_device(int(gpu))
        device = "cuda" if torch.cuda.is_available() else "cpu"
    else:
        device = 'cpu'
    #print("use device:%s" % device)
    prefix0 = prefix
    if config_predict.prefixTrim:
        prefix = sentTriming(prefix0)
        if len(prefix)==0:
            prefix = prefix0
    punc = '.,?!;\t 。，？！；'
    global a
    a = app
    fast_pattern = config_predict.fast_pattern
    n_ctx = model.config.n_ctx
    len_prefix = len(prefix)
    if len_prefix<5:
        max_genlen = 5*len_prefix
    elif len_prefix<10:
        max_genlen = 3*len_prefix
    else:
        max_genlen = config['length']
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
    raw_text = prefix
    context_tokens = tokenizer.convert_tokens_to_ids(tokenizer.tokenize(raw_text))
    t0 = time.time()
    S = []
    rev_repitition_penalty = 1.0 / repetition_penalty
    inputs = [context_tokens] * nsamples
    inputs = torch.tensor(inputs, dtype=torch.long, device=device)
    _, past = model(inputs[:, :-1], None)[:2]
    prev = inputs[:, -1].view(-1, 1)
    context = context_tokens
    generate = [[t for t in context] for _ in range(nsamples)]
    A0 = []
    A1 = []
    for kk in range(len(generate)):
        for jj in range(len(generate[kk])):
            A0.append(kk)
            A1.append(generate[kk][jj])
    with torch.no_grad():
        for i in range(nsamples):
            output = model(prev, past=past)
            output, past = output[:2]
            output = output.squeeze(1)
            output[A0, A1] *= rev_repitition_penalty
            output /= temperature
            filtered_logits = top_k_top_p_filtering(output, top_k=topk, top_p=0)
            next_token = torch.multinomial(torch.softmax(filtered_logits, dim=-1), num_samples=1)
            prev = next_token
            NT_np = next_token.cpu().numpy()
            for ii in range(nsamples):
                generate[ii].append(NT_np[ii][0])
                A0.append(ii)
                A1.append(NT_np[ii])
    outs = generate
    for out in outs:
        tmptext = untokenization(out, config, tokenizer, punc, continue_writing)
        S.append(tmptext)
    return S
    outs = fast_sample_sequence_batch(model, context_tokens, length, nsamples=maxNb,
                                      temperature=temperature, top_k=topk, repitition_penalty=repetition_penalty,
                                      device=device)
    return outs
    for out in outs:
        tmptext = untokenization(out, config, tokenizer, punc, continue_writing)
        S.append(tmptext)

    t1 = time.time()
    if config_predict.prefixTrim:
        S = [prefix0+s[len(prefix):] for s in S]
    S = postprocess(S,prefix0,config_predict,removeHighFreqWords=removeHighFreqWords)
    S = dropDuplicateContent(S)
    if config_predict.resort:
        if len(S)>0:
            S = resort(prefix0, S, config_predict)
    t2 = time.time()
    #print('text generating and posprocess time:%0.4f and %0.4f' % (t1 - t0,t2-t1))
    S = S[:nsamples]
    return S
def testFun1():
    import numpy as np
    for _ in range(20):
        a = np.random.uniform(-1,1,(10,10000))
        b = np.random.uniform(-1,1,(10000,10))
        c = a.dot(b)
def fast_sample_sequence_batch_poemHead(model, contexts, inputs,length, nsamples=10,temperature=1.0, top_k=30, repitition_penalty=1.0, device='cpu'):
    #inputs = torch.LongTensor(context).view(1, -1).to(device)
    rev_repitition_penalty = 1.0 / repitition_penalty
    #inputs = [context] * nsamples
    inputs = torch.tensor(inputs, dtype=torch.long, device=device)
    _, past = model(inputs[:, :-1], None)[:2]
    #prev = inputs[:, -1].view(1, -1)
    prev = inputs[:, -1].view(-1, 1)
    generate = contexts
    A0 = []
    A1 = []
    for kk in range(len(generate)):
        for jj in range(len(generate[kk])):
            A0.append(kk)
            A1.append(generate[kk][jj])
    with torch.no_grad():
        for i in range(length):
            #now = datetime.now()
            output = model(prev, past=past)
            #then = datetime.now()
            #a.logger.info('for : {}'.format(then - now))
            output, past = output[:2]
            #output = output[-1].squeeze(0) / temperature
            output = output.squeeze(1)
            output[A0, A1] *= rev_repitition_penalty
            output /= temperature
            filtered_logits = top_k_top_p_filtering(output, top_k=top_k, top_p=0)
            next_token = torch.multinomial(torch.softmax(filtered_logits, dim=-1), num_samples=1)
            #generate.append(next_token.item())
            #prev = next_token.view(1, 1)
            prev = next_token
            NT_np = next_token.cpu().numpy()
            for ii in range(nsamples):
                generate[ii].append(NT_np[ii][0])
                A0.append(ii)
                A1.append(NT_np[ii])
    return generate

def generating_poem_head(prefix,model,config,tokenizer,device,config_predict,num=20,lens = [5,7],sents=4,gpu='0'):
    if len(prefix) == 0 or len(prefix) > 10:
        return []
    if gpu:
        torch.cuda.set_device(int(gpu))
        device = "cuda" if torch.cuda.is_available() else "cpu"
    else:
        device = 'cpu'
    nsamples = num
    temperature = config['temperature']
    topk = config['topk']
    repetition_penalty = config['repetition_penalty']
    punc_mid = '，'
    punc_end = '。！？'
    def getpoem(len_sent,nb_sents):
        #len_sent = 7
        #nb_sents = 8
        if len(prefix)<nb_sents:
            prefix0 = list(prefix)+['']*(nb_sents-len(prefix)+1)
        else:
            prefix0 = list(prefix)
        raw_text = prefix0[0]
        id_msk = tokenizer.convert_tokens_to_ids('[MASK]')
        context = [id_msk] + tokenizer.convert_tokens_to_ids(tokenizer.tokenize(raw_text))
        contexts = [[c for c in context] for _ in range(int(nsamples/2))]
        inputs = [[c for c in context] for _ in range(int(nsamples/2))]
        num = int(nsamples/2)
        for ii in range(1,nb_sents+1):
            outs = fast_sample_sequence_batch_poemHead(model, contexts, inputs, length=len_sent+1, nsamples=num, temperature=temperature, top_k=topk,
                                                repitition_penalty=repetition_penalty, device=device)
            S = [untokenization_poem(out, tokenizer, config) for out in outs]
            if ii==nb_sents:
                break
            S = [tmptext for tmptext in S if len(tmptext)>ii * (len_sent+1)-1]
            if ii % 2 == 0:
                S1 = [tt[:ii * (len_sent+1)] for tt in S if tt[ii * (len_sent+1)-1] in punc_end]
            else:
                S1 = [tt[:ii * (len_sent+1)] for tt in S if tt[ii * (len_sent+1)-1] in punc_mid]
            raw_texts = [s+prefix0[ii] for s in S1]
            num = len(raw_texts)
            contexts = [[id_msk]+tokenizer.convert_tokens_to_ids(tokenizer.tokenize(raw)) for raw in raw_texts]
            inputs = contexts
            if num==0:
                break
        R = []
        for s in S:
            if s[-1] not in punc_end:
               t = s + '。'
            else:
                t = s
            poem = poemFilter1(t,prefix,config_predict.blackwords)
            if poem:
                R.append(poem)
        return R
    R = []
    for len_sent in lens:
        R.extend(getpoem(len_sent, sents))
    random.shuffle(R)
    return R
