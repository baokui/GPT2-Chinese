import re
import html
import os
import urllib.parse
from html import escape
import codecs
from urllib.parse import unquote
import torch
import torch.nn.functional as F
import os
import argparse
from tqdm import trange
from transformers import GPT2LMHeadModel
import json
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
def generating(prefix,model,config,tokenizer):
    n_ctx = model.config.n_ctx
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
                    elif item == '[PAD]':
                        text[i] = ''
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
                S.append(tmptext)
        if len(S) == nsamples:
            break
    return S
model,tokenizer,config = getModel(path_config='config.json')
model_pr,tokenizer_pr,config_pr = getModel(path_config='config_pretrained.json')
def application(environ, start_response):

    start_response('200 OK', [('Content-Type', 'text/html')])

    f = open("text1.html","r",encoding="utf-8")

    b = f.read()

    # the environment variable CONTENT_LENGTH may be empty or missing
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0
    # When the method is POST the query string will be sent
    # in the HTTP request body which is passed by the WSGI server
    # in the file like wsgi.input environment variable.
    request_body = environ['wsgi.input'].read(request_body_size)
    #request_body = str(request_body, encoding="utf-8")
    print(request_body)
    try:
        request_body = unquote(request_body, encoding="utf-8")
    except:
        request_body = str(request_body, encoding="utf-8")
    print(request_body)
    d = urllib.parse.parse_qs(request_body,encoding='utf-8')
    if len(d)>=1:
        inputStr = d.get('inputStr', [''])[0]  # Returns the first age value.
        #inputStr = str(inputStr, encoding="utf-8")
        inputStr = html.unescape(inputStr)
    else:
        inputStr = ""
    body = re.sub("{tittle}", 'python Web', b)

    body1 = re.sub("{content}", 'hello pyweb!', body)
    if inputStr=="":
        body2 = body1 % ('Empty',
                         '<br>'.join(['No results']),
                         '<br>'.join(['No results']))

        f.close()
        return [body2.encode()]
    hobbies = d.get('hobbies', [])  # Returns a list of hobbies.
    # Always escape user input to avoid script injection
    print('input:%s'%inputStr)
    result = generating(inputStr,model,config,tokenizer)
    result_pr = generating(inputStr,model_pr,config_pr,tokenizer_pr)
    #result = ['a','b']
    #result_pr = ['cd','d']
    result = ['\t'+str(i)+'. '+result[i] for i in range(len(result))]
    result_pr = ['\t' + str(i) + '. ' + result_pr[i] for i in range(len(result_pr))]
    print("result-fineture:%s"%'\n'.join(result))
    print("result-pretrain:%s"%'\n'.join(result_pr))
    hobbies = [escape(hobby) for hobby in result]
    hobbies_pr = [escape(hobby) for hobby in result_pr]
    body = re.sub("{tittle}",'python Web',b)

    body1 = re.sub("{content}",'hello pyweb!',body)

    #age = "33"
    #hobbies = ['a', 'b']
    #inputStr = bytes(inputStr, encoding="utf8")
    body2 = body1 % (inputStr or 'Empty',
                            '<br>'.join(hobbies or ['No Hobbies']),
                            '<br>'.join(hobbies_pr or ['No Hobbies']))

    f.close()

    return [body2.encode()]