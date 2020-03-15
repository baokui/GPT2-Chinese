import sys
import os
import shutil
import tqdm
from tokenizations import tokenization_bert
import random
from collections import Counter
def build_files(data_path, dataname, tokenized_data_path, full_tokenizer,n_ctx = 50, min_length=20,num_pieces=1, max_nb = 10000000):
    if not os.path.exists(tokenized_data_path):
        os.mkdir(tokenized_data_path)
    k = 0
    full_line = []
    print('reading lines')
    nb_lines = 0
    for ii in range(5):
        f = open(data_path+'/part-0000'+str(ii), 'r', encoding='utf8')
        for line in f:
            tmp = line.strip().split('\t')
            if len(tmp)!=2:
                continue
            line = tmp[1]
            if nb_lines%10000==0:
                print('processing file %s, %d, %0.2f'%(data_path,nb_lines,nb_lines/float(max_nb)))
            if len(line)<min_length:
                continue
            nb_lines += 1
            subline = full_tokenizer.convert_tokens_to_ids(list(line))
            #print(full_tokenizer.convert_tokens_to_ids('[MASK]'))
            #print(subline)
            #print(full_tokenizer.convert_tokens_to_ids('[CLS]'))
            tmp = [full_tokenizer.convert_tokens_to_ids('[MASK]')]
            tmp = tmp + subline
            if len(tmp)>n_ctx-1:
                tmp = tmp[:n_ctx-1]
            else:
                tmp = tmp+(n_ctx-1-len(tmp))*[full_tokenizer.convert_tokens_to_ids('[PAD]')]
            tmp = tmp + [full_tokenizer.convert_tokens_to_ids('[CLS]')]
            full_line.extend(tmp)
            if nb_lines>=max_nb:
                with open(tokenized_data_path + dataname+'-{}.txt'.format(k), 'w') as f:
                    for id in full_line:
                        f.write(str(id) + ' ')
                k += 1
                full_line = []
                nb_lines = 0
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
def build_files_seg(data_path, dataname, tokenized_data_path, full_tokenizer,n_ctx = 20, min_length=5,num_pieces=1, max_nb = 10000000):
    if not os.path.exists(tokenized_data_path):
        os.mkdir(tokenized_data_path)
    k = 0
    full_line = []
    print('reading lines')
    nb_lines = 0
    f = open(data_path, 'r', encoding='utf8')
    for line in f:
        tmp = line.strip().split('\t')
        if len(tmp)!=2:
            continue
        line = tmp[1]
        if nb_lines%10000==0:
            print('processing file %s, %d, %0.2f'%(data_path,nb_lines,nb_lines/float(max_nb)))
        if len(line)<min_length:
            continue
        nb_lines += 1
        subline = full_tokenizer.convert_tokens_to_ids(list(line))
        #print(full_tokenizer.convert_tokens_to_ids('[MASK]'))
        #print(subline)
        #print(full_tokenizer.convert_tokens_to_ids('[CLS]'))
        tmp = [full_tokenizer.convert_tokens_to_ids('[MASK]')]
        tmp = tmp + subline
        if len(tmp)>n_ctx-1:
            tmp = tmp[:n_ctx-1]
        else:
            tmp = tmp+(n_ctx-1-len(tmp))*[full_tokenizer.convert_tokens_to_ids('[PAD]')]
        tmp = tmp + [full_tokenizer.convert_tokens_to_ids('[CLS]')]
        full_line.extend(tmp)
        if nb_lines>=max_nb:
            with open(tokenized_data_path + dataname+'-{}.txt'.format(k), 'w') as f:
                for id in full_line:
                    f.write(str(id) + ' ')
            k += 1
            full_line = []
            nb_lines = 0
    f.close()
    print('finish')

def main(data_path,dataname):
    tokenizer_path = '../model/gpt2_prose/vocab.txt'
    tokenized_data_path = '../data/dabaigou_tokenized_new/'
    full_tokenizer = tokenization_bert.BertTokenizer(vocab_file=tokenizer_path)
    build_files(data_path, dataname, tokenized_data_path, full_tokenizer)
    shutil.rmtree(data_path)
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
        data_path,dataname = sys.argv[2:4]
        main(data_path,dataname)
    if mode=='word':
        data_path, dataname = sys.argv[2:4]
        main_seg(data_path, dataname)