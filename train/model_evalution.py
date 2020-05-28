import torch
import torch.nn.functional as F
from test import *
import sys
def getmodel(path_config,gpu='3'):
    from Config import Config
    ConfigPredict = config_predict(model_config=path_config,gpus=gpu)
    path_configs = ConfigPredict.model_configs
    model,tokenizer,config,device = getModel(path_config=path_configs,gpu=gpu)
    config['repetition_penalty'] = ConfigPredict.repetition_penalty
    config['temperature'] = ConfigPredict.temperature
    config['length'] = ConfigPredict.length
    return model,config,tokenizer,ConfigPredict
def getppl(model, context_tokens,tokenizer,device='cpu'):
    #inputs = torch.LongTensor(context).view(1, -1).to(device)
    length = len(context_tokens)
    n_ctx = model.config.n_ctx
    length = min(length,n_ctx-1)
    P = []
    with torch.no_grad():
        for idx in range(1,length):
            context = torch.tensor(context_tokens[:idx], dtype=torch.long, device=device)
            context = context.unsqueeze(0)
            generated = context
            inputs = {'input_ids': generated[0][-(n_ctx - 1):].unsqueeze(0)}
            outputs = model(
                **inputs)  # Note: we could also use 'past' with GPT-2/Transfo-XL/XLNet (cached hidden-states)
            next_token_logits = outputs[0][0, -1, :]
            #next_token_logits[tokenizer.convert_tokens_to_ids('[UNK]')] = -float('Inf')
            #filtered_logits = top_k_top_p_filtering(next_token_logits, top_k=top_k, top_p=top_p)
            filtered_logits = next_token_logits
            next_token_prob = F.softmax(filtered_logits, dim=-1)
            p = next_token_prob[context_tokens[idx]]
            P.append(p.cpu().numpy())
    S = 1
    for p in P:
        S *= p
    ppl = S**(-1/(length-1))
    return ppl
def main(path_config,path_data):
    model, config, tokenizer, ConfigPredict = getmodel(path_config)
    device = 'cuda'
    with open(path_data,'r') as f:
        data = f.read().strip().split('\n')
    PPL = []
    for s in data:
        id_msk = tokenizer.convert_tokens_to_ids('[MASK]')
        context_tokens = [id_msk] + tokenizer.convert_tokens_to_ids(tokenizer.tokenize(s))
        ppl = getppl(model, context_tokens,tokenizer,device)
        PPL.append(ppl)
    idx0 = path_config.find('config_')+len('config_')
    path_target = path_data[:-4]+'_'+path_config[idx0:-5]+'-ppl.txt'
    m = sum(PPL)/len(PPL)
    S = [['mean','%0.4f'%m]]
    for i in range(len(PPL)):
        S.append([data[i],'%0.4f'%PPL[i]])
    S = ['\t'.join(s) for s in S]
    with open(path_target,'w') as f:
        f.write('\n'.join(S))
if __name__=='__main__':
    path_config,path_data = sys.argv[1:3]
    main(path_config, path_data)
