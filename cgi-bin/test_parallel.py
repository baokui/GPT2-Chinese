from testing import *
def getModel(path_config):
    with open(path_config,'r') as f:
        config = json.load(f)
    from tokenizations import tokenization_bert
    tokenizer_path = config['tokenizer_path']
    model_path = config['model_path']
    device = 'cuda'
    tokenizer = tokenization_bert.BertTokenizer(vocab_file=tokenizer_path)
    model = GPT2LMHeadModel.from_pretrained(model_path)
    model.to(device)
    model.eval()
    return model,tokenizer,config
path_source='data/input_poem.txt'
path_config='config/config_poem.json'
model, tokenizer, config = getModel(path_config=path_config)
with open(path_source, 'r') as f:
    lines = f.read().strip().split('\n')
i = 0
inputStr = lines[i].strip().lower()
segment,modelType=False,'poem'
prefix = inputStr
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
device = 'cuda'

S = generating(prefix,model,config,tokenizer,segment=False,nsamples=10,modelType='poem')
S = generating1(prefix,model,config,tokenizer,segment=False,nsamples=10,modelType='poem')
def fast_sample_sequence(model, context_tokens, length, nsamples = 10,temperature=1.0, top_k=30, top_p=0.0, device='cpu'):
    context = [[context_tokens] for i in range(nsamples)]
    # context = context_tokens
    inputs = torch.LongTensor(context).view(1, -1).to(device)
    inputs = torch.reshape(inputs, (nsamples, len(context_tokens)))
    _, past = model(inputs[:, :-1], None)[:2]
    prev = inputs[:, -1].view(1, -1)
    prev = torch.reshape(prev, (nsamples, 1))
    generate = [context_tokens for i in range(nsamples)]
    with torch.no_grad():
        for i in trange(length):
            past0 = (past[0][:, :1, :, :, :], past[1][:, :1, :, :, :], past[2][:, :1, :, :, :], past[3][:, :1, :, :, :])
            for ii in range(len(past)):
                for jj in range(nsamples):
                    past[ii][:, jj, :, :, :] = past0[ii][:, 0, :, :, :]
            output = model(prev, past=past)
            output, past = output[:2]
            prev_ = []
            for k in range(nsamples):
                output1 = output[k].squeeze(0) / temperature
                filtered_logits = top_k_top_p_filtering(output1, top_k=top_k, top_p=top_p)
                next_token = torch.multinomial(torch.softmax(filtered_logits, dim=-1), num_samples=1)
                generate[k].append(next_token.item())
                prev_.append(next_token.item())
            prev = torch.tensor(prev_)
            prev = torch.reshape(prev, (nsamples, 1))
    return generate
def sample_sequence(model, context_tokens, length, n_ctx, tokenizer, nsamples,temperature=1.0, top_k=30, top_p=0.0, repitition_penalty=1.0,
                    device='cpu'):
    n = nsamples
    context = [[context_tokens]*n]
    context = torch.tensor(context, dtype=torch.long, device=device)
    context = context.squeeze(0)
    generated = context
    with torch.no_grad():
        for _ in trange(length):
            inputs = {'input_ids': generated[:,-(n_ctx - 1):].unsqueeze(0)}
            outputs = model(
                **inputs)  # Note: we could also use 'past' with GPT-2/Transfo-XL/XLNet (cached hidden-states)
            next_token_logits = outputs[0][0,:, -1, :]
            for ii in range(n):
                for id in set(generated[ii]):
                    next_token_logits[ii][id] /= repitition_penalty
            next_token_logits = next_token_logits / temperature
            Next = []
            for ii in range(n):
                next_token_logits[ii][tokenizer.convert_tokens_to_ids('[UNK]')] = -float('Inf')
                filtered_logits = top_k_top_p_filtering(next_token_logits[ii], top_k=top_k, top_p=top_p)
                next_token = torch.multinomial(F.softmax(filtered_logits, dim=-1), num_samples=1)
                Next.append(torch.reshape(next_token,(1,1)))
            #next_token = torch.tensor(Next)
            next_token = torch.cat(Next,dim=0)
            generated = torch.cat((generated, next_token), dim=1)
    return generated.tolist()
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
    #print('generating-begin for %s'%prefix)
    raw_text = prefix
    #print(raw_text)
    if segment:
        context_tokens = tokenizer_seg(list(jieba.cut(raw_text)))
    else:
        context_tokens = tokenizer.convert_tokens_to_ids(tokenizer.tokenize(raw_text))
    #print(context_tokens)
    generated = 0
    #print(n_ctx, context_tokens, length, fast_pattern, temperature, topk, topp, repetition_penalty, device)
    Out = fast_sample_sequence(model, context_tokens, length,nsamples=nsamples,temperature=temperature, top_k=topk, top_p=topp, device=device)
    S = []
    for out in Out:
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
    return S

def generating1(prefix,model,config,tokenizer,segment=False,nsamples=10,modelType='other'):
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
    device = 'cuda'
    if length == -1:
        length = model.config.n_ctx
    #print('generating-begin for %s'%prefix)
    raw_text = prefix
    #print(raw_text)
    if segment:
        context_tokens = tokenizer_seg(list(jieba.cut(raw_text)))
    else:
        context_tokens = tokenizer.convert_tokens_to_ids(tokenizer.tokenize(raw_text))
    #print(context_tokens)
    generated = 0
    #print(n_ctx, context_tokens, length, fast_pattern, temperature, topk, topp, repetition_penalty, device)
    Out = sample_sequence(model, context_tokens, length, n_ctx, tokenizer,nsamples,temperature=temperature, top_k=topk, top_p=topp, device=device)
    S = []
    for out in Out:
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
    return S

repitition_penalty = config['repetition_penalty']
n=2
context = [[context_tokens]*n]
context = torch.tensor(context, dtype=torch.long, device=device)
context = context.squeeze(0)
generated = context
with torch.no_grad():
    for _ in trange(length):
        inputs = {'input_ids': generated[0][-(n_ctx - 1):].unsqueeze(0)}
        outputs = model(
            **inputs)  # Note: we could also use 'past' with GPT-2/Transfo-XL/XLNet (cached hidden-states)
        next_token_logits = outputs[0][0,:, -1, :]
        for ii in range(n):
            for id in set(generated[ii]):
                next_token_logits[ii][id] /= repitition_penalty
        next_token_logits = next_token_logits / temperature
        Next = []
        for ii in range(n):
            next_token_logits[ii][tokenizer.convert_tokens_to_ids('[UNK]')] = -float('Inf')
            filtered_logits = top_k_top_p_filtering(next_token_logits[ii], top_k=top_k, top_p=top_p)
            next_token = torch.multinomial(F.softmax(filtered_logits, dim=-1), num_samples=1)
            Next.append(next_token.item())
        next_token = torch.tensor(Next)
        next_token = torch.reshape(next_token, (n, 1))
        generated = torch.cat((generated, next_token), dim=1)