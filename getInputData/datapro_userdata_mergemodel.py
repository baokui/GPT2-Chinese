import sys
import os
from tokenizations import tokenization_bert
def token_pad(line,vocab,n_ctx):
    punc = '.;!?。；！？'
    S = [line[0]]
    for i in range(1,len(line)):
        if line[i-1] in punc and line[i]=='，':
            continue
        S.append(line[i])
    T = []
    t = [str(vocab.index('[MASK_gou]'))]
    for s in S:
        if s in vocab:
            t.append(str(vocab.index(s)))
        else:
            t.append(str(vocab.index('[UNK]')))
        if len(t)==n_ctx-1:
            t.append(str(vocab.index('[CLS]')))
            T.append(' '.join(t))
            t = [str(vocab.index('[MASK_gou]'))]
    return T
def build_files(data_path, dataname, tokenized_data_path, full_tokenizer, idx, n_ctx=64,min_length=10,padding=False):
    if not os.path.exists(tokenized_data_path):
        os.mkdir(tokenized_data_path)
    print('reading lines')
    nb_lines = 0
    files = os.listdir(data_path)
    for file in files:
        if 'part' not in file:
            continue
        if int(file[7:9])!=idx:
            continue
        nb_samples =  0
        print(file)
        f = open(os.path.join(data_path,file), 'r', encoding='utf8')
        f_w = open(os.path.join(tokenized_data_path, dataname+file[-1]+'.txt'), 'a+')
        for line in f:
            if len(line)<min_length:
                continue
            full_line = token_pad(line,full_tokenizer,n_ctx)
            if len(full_line)==0:
                continue
            nb_samples+=len(full_line)
            if nb_lines%10000==0:
                print('processing file %s with %d lines %d samples'%(file,nb_lines,nb_samples))
            nb_lines += 1
            f_w.write('\n'.join(full_line)+'\n')
        f_w.close()
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

def main(data_path,idx,dataname,tokenized_data_path,path_vocab,padding):
    #tokenizer_path = '../data/vocab/vocab_god_userdata.txt'
    #tokenized_data_path = '../data/userdata_tokenized_new/'
    with open(path_vocab,'r') as f:
        full_tokenizer = f.read().strip().split('\n')
    #full_tokenizer = tokenization_bert.BertTokenizer(vocab_file=path_vocab)
    build_files(data_path, dataname, tokenized_data_path, full_tokenizer,idx,padding=padding)
    #shutil.rmtree(data_path)

if __name__=='__main__':
    data_path,idx,dataname,tokenized_data_path,path_vocab,padding = sys.argv[1:7]
    idx = int(idx)
    padding = padding=='1'
    main(data_path,idx,dataname,tokenized_data_path,path_vocab,padding)
