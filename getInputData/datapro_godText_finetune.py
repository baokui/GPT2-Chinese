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
def build_files(full_tokenizer,path_source,path_target,padding,sym='',n_ctx=64,min_length=10,nb_piece=10):
    if not os.path.exists(path_target):
        os.mkdir(path_target)
    punc = '。？！'
    full_line = []
    print('reading lines')
    nb_lines = 0
    lines = []
    for ii in range(5):
        with open(path_source+'/part-0000'+str(ii),'r') as f:
            lines0 = f.read().strip().split('\n')
        if len(lines0)>1:
            lines.extend([line.split('\t')[-1] for line in lines0])
    for line in lines:
        nb_lines += 1
        if len(line)<min_length:
            continue
        if line[-1] not in punc:
            continue
        subline = full_tokenizer.convert_tokens_to_ids(list(line))
        if padding:
            tmp,line = token_pad(line,full_tokenizer,subline,n_ctx)
            full_line.extend(tmp)
            while len(line)>n_ctx:
                tmp, line = token_pad(line,full_tokenizer,subline,n_ctx)
                full_line.extend(tmp)
        else:
            tmp = [full_tokenizer.convert_tokens_to_ids('[MASK]')]
            tmp = tmp + subline
            tmp = tmp + [full_tokenizer.convert_tokens_to_ids('[CLS]')]
            full_line.extend(tmp)
        if nb_lines%100000==0:
            print('processing file %s with %d lines'%(path_source,nb_lines))
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
def changenames():
    path = './data/sogouInput_tokenized/'
    filename_list = os.listdir(path)
    for i in range(len(filename_list)):
        file = filename_list[i]
        oldpath = os.path.join(path,file)
        newpath = oldpath[:len(path)]+'tokenized_train_{}.txt'.format(i)
        os.rename(oldpath, newpath)
        if i%100==0:
            print(i,oldpath,newpath)

def main(path_source,path_target,padding,path_vocab,nb_piece,n_ctx,sym):
    #tokenizer_path = '../data/vocab/vocab_god_userdata.txt'
    #tokenized_data_path = '../data/userdata_tokenized_new/'
    full_tokenizer = tokenization_bert.BertTokenizer(vocab_file=path_vocab)
    build_files(full_tokenizer,path_source,path_target,padding,nb_piece=nb_piece,n_ctx=n_ctx,sym=sym)
    #shutil.rmtree(data_path)
def main_seg(data_path,dataname):
    tokenizer_path = '../model/model_dabaigou_seg/vocab.txt'
    tokenized_data_path = '../data/dabaigou_tokenized_seg/'
    full_tokenizer = tokenization_bert.BertTokenizer(vocab_file=tokenizer_path)
    build_files_seg(data_path, dataname, tokenized_data_path, full_tokenizer)
    #shutil.rmtree(data_path)
def remove_unk(idx = 0,unk='100'):
    def count_list(std: list, tongji):
        name = Counter()
        for num in std:
            name[num] += 1
        return name[tongji]
    tokenized_data_path = '../data/dabaigou_tokenized_new/'
    tokenized_data_path1 = '../data/dabaigou_tokenized_new1/'
    files = os.listdir(tokenized_data_path)
    k = 0
    for file in files:
        if k<idx or k>idx+30:
            k += 1
            continue
        f = open(os.path.join(tokenized_data_path,file),'r')
        s = f.read().strip().split()
        f.close()
        R = [s[i*50:(i+1)*50] for i in range(int(len(s)/50))]
        i = 0
        S = []
        for r in R:
            if count_list(r, '100')<2:
                S.extend(r)
            if i%100000==0:
                print('file-{}(total:{}),line-{}(total:{})'.format(k,len(files),int(i/100000),int(len(R)/100000)))
            i += 1
        k += 1
        with open(os.path.join(tokenized_data_path1,file),'w') as f:
            f.write(' '.join(S))

if __name__=='__main__':
    path_source,path_target,padding,path_vocab,nb_piece,n_ctx,sym = sys.argv[1:]
    padding = padding=='1'
    main(path_source,path_target,padding,path_vocab,int(nb_piece),int(n_ctx),sym)