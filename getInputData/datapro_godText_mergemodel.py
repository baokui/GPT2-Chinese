import sys
import os
import json
def token_pad(line,vocab,n_ctx):
    punc = '.;!?。；！？'
    S = [line[0]]
    for i in range(1,len(line)):
        if line[i-1] in punc and line[i]=='，':
            continue
        S.append(line[i])
    T = []
    t = [str(vocab.index('[MASK_prose]'))]
    for s in S:
        if s in vocab:
            t.append(str(vocab.index(s)))
        else:
            t.append(str(vocab.index('[UNK]')))
        if len(t)==n_ctx-1:
            t.append(str(vocab.index('[CLS]')))
            T.append(' '.join(t))
            t = [str(vocab.index('[MASK_prose]'))]
    return T
def build_files(data_path, tokenized_data_path, full_tokenizer, n_ctx=64,min_length=10,maxlines=200000):
    if not os.path.exists(tokenized_data_path):
        os.mkdir(tokenized_data_path)
    print('reading lines')
    nb_lines = 0
    with open(data_path,'r') as f:
        S = json.load(f)
    idx = 0
    nb_samples = 0
    T = []
    for line in S:
        if len(line)<min_length:
            continue
        full_line = token_pad(line,full_tokenizer,n_ctx)
        if len(full_line)==0:
            continue
        T.extend(full_line)
        nb_samples+=len(full_line)
        if nb_lines%10000==0:
            print('processing file %s with %d lines %d samples'%(data_path,nb_lines,nb_samples))
        nb_lines += 1
        if len(T)>=maxlines:
            with open(os.path.join(tokenized_data_path, str(idx)+'.txt'), 'w') as f_w:
                f_w.write('\n'.join(T)+'\n')
            idx+=1
            T = []
    with open(os.path.join(tokenized_data_path, str(idx) + '.txt'), 'w') as f_w:
        f_w.write('\n'.join(T) + '\n')
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

def main(data_path,tokenized_data_path,path_vocab,padding):
    #tokenizer_path = '../data/vocab/vocab_god_userdata.txt'
    #tokenized_data_path = '../data/userdata_tokenized_new/'
    with open(path_vocab,'r') as f:
        full_tokenizer = f.read().strip().split('\n')
    #full_tokenizer = tokenization_bert.BertTokenizer(vocab_file=path_vocab)
    build_files(data_path, tokenized_data_path, full_tokenizer,padding=padding)
    #shutil.rmtree(data_path)

if __name__=='__main__':
    data_path,tokenized_data_path,path_vocab,padding = sys.argv[1:5]
    padding = padding=='1'
    main(data_path,tokenized_data_path,path_vocab,padding)
