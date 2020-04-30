import json
import sys
import os
import shutil
import json
from tokenizations import tokenization_bert
from collections import Counter
def token_pad(line,full_tokenizer,subline,n_ctx):
    punc = '.;!?。；！？'
    tmp = [full_tokenizer.convert_tokens_to_ids('[MASK]')]
    tmp = tmp + subline
    if len(tmp) > n_ctx - 1:
        tmp = tmp[:n_ctx - 1]
        idx_b = n_ctx-1
    else:
        tmp = tmp + (n_ctx - 1 - len(tmp)) * [full_tokenizer.convert_tokens_to_ids('[PAD]')]
        idx_b = len(line)
    line = line[idx_b:]
    idx0 = 0
    for p in punc:
        if p in line:
            idx0 = line.index(p)+1
            break
    line = line[idx0:]
    tmp = tmp + [full_tokenizer.convert_tokens_to_ids('[CLS]')]
    return tmp,line
def build_files(full_tokenizer,path_source,path_target,sym='',n_ctx=74,nb_piece=10):
    if not os.path.exists(path_target):
        os.mkdir(path_target)
    with open(path_source,'r') as f:
        lines = json.load(f)
    full_line = []
    for line in lines:
        subline = full_tokenizer.convert_tokens_to_ids(list(line))
        tmp,line = token_pad(line,full_tokenizer,subline,n_ctx)
        full_line.extend(tmp)
        while len(line)>n_ctx:
            tmp, line = token_pad(line,full_tokenizer,subline,n_ctx)
            full_line.extend(tmp)
    i0 = 0
    num = int(len(full_line)/(nb_piece*n_ctx))
    i1 = i0 + num*n_ctx
    k = 0
    while i0<len(full_line):
        with open(os.path.join(path_target,sym+'godTokenizer_'+str(k)+'.txt'), 'w') as f:
            s = [str(full_line[i]) for i in range(i0,min(i1,len(full_line)))]
            f.write(' '.join(s))
        i0 = i1
        i1 = i0 + num*n_ctx
        k+=1
    print('finish')
def getPoem(path_source,path_target,keywords=''):
    if keywords=='':
        keywords = ['爱', '情', '相思', '相忆','美人']
    with open(path_source,'r',encoding='utf-8') as f:
        s = json.load(f)
    R = []
    for t in s:
        for key in keywords:
            if key in t:
                R.append(t)
                break
    with open(path_target,'w',encoding='utf-8') as f:
        json.dump(R,f,ensure_ascii=False,indent=4)
def main(path_source,path_target,path_vocab,nb_piece,n_ctx):
    #tokenizer_path = '../data/vocab/vocab_god_userdata.txt'
    #tokenized_data_path = '../data/userdata_tokenized_new/'
    full_tokenizer = tokenization_bert.BertTokenizer(vocab_file=path_vocab)
    build_files(full_tokenizer,path_source,path_target,nb_piece=nb_piece,n_ctx=n_ctx)
    #shutil.rmtree(data_path)
if __name__=='__main__':
    path_source,path_target,path_vocab,nb_piece,n_ctx = sys.argv[1:6]
    nb_piece, n_ctx = int(nb_piece),int(n_ctx)
    main(path_source, path_target, path_vocab, nb_piece, n_ctx)