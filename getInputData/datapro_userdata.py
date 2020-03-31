import sys
import os
import shutil
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
def build_files(data_path, dataname, tokenized_data_path, full_tokenizer, idx, n_ctx=64,min_length=10,padding=False):

    if not os.path.exists(tokenized_data_path):
        os.mkdir(tokenized_data_path)
    full_line = []
    print('reading lines')
    nb_lines = 0
    files = os.listdir(data_path)
    for file in files:
        if 'part' not in file:
            continue
        if int(file[7:9])!=idx:
            continue
        f = open(os.path.join(data_path,file), 'r', encoding='utf8')
        for line in f:
            nb_lines += 1
            if len(line)<min_length:
                continue
            subline = full_tokenizer.convert_tokens_to_ids(list(line))
            if padding:
                tmp,line = token_pad(full_tokenizer,subline,n_ctx)
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
                print('processing file %s with %d lines'%(file,nb_lines))
        with open(os.path.join(tokenized_data_path,dataname), 'w') as f:
            for id in full_line:
                f.write(str(id) + ' ')
        f.close()
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

def main(data_path,idx,dataname,tokenized_data_path,padding):
    tokenizer_path = '../model/gpt2_prose/vocab.txt'
    #tokenized_data_path = '../data/userdata_tokenized_new/'
    full_tokenizer = tokenization_bert.BertTokenizer(vocab_file=tokenizer_path)
    build_files(data_path, dataname, tokenized_data_path, full_tokenizer,idx,padding=padding)
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
    mode = sys.argv[1]
    if mode=='char':
        data_path,idx,dataname,tokenized_data_path,padding = sys.argv[2:7]
        idx = int(idx)
        padding = padding=='1'
        main(data_path,idx,dataname,tokenized_data_path,padding)
    if mode=='word':
        data_path, dataname = sys.argv[2:4]
        main_seg(data_path, dataname)