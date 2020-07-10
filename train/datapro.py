import sys
import os
from collections import Counter
def token_pad(line,full_tokenizer,subline,n_ctx,token_mask='[MASK]'):
    punc = '.;!?。；！？'
    tmp = [full_tokenizer.index(token_mask)]
    tmp = tmp + subline
    if len(tmp) > n_ctx - 1:
        tmp = tmp[:n_ctx - 1]
        idx_b = n_ctx-1
    else:
        tmp = tmp + (n_ctx - 1 - len(tmp)) * [full_tokenizer.index('[PAD]')]
        idx_b = len(line)
    line = line[idx_b:]
    idx0 = 0
    for p in punc:
        if p in line:
            idx0 = line.index(p)+1
            break
    line = line[idx0:]
    tmp = tmp + [full_tokenizer.index('[CLS]')]
    tmp = ' '.join([str(ss) for ss in tmp])
    return tmp,line
def build_files(path_source,path_target, full_tokenizer,token_mask,maxline, n_ctx=64,min_length=10,padding=True):
    full_line = []
    print('reading lines')
    nb_lines = 0
    files = os.listdir(path_source)
    idx = 0
    for file in files:
        if 'part' not in file:
            continue
        f = open(os.path.join(path_source,file), 'r', encoding='utf8')
        for line in f:
            nb_lines += 1
            line = line.strip().split('\t')[-1]
            if len(line)<min_length:
                continue
            subline = []
            for a in line:
                if a in full_tokenizer:
                    subline.append(full_tokenizer.index(a))
                else:
                    subline.append(full_tokenizer.index('[UNK]'))
            if padding:
                tmp,line = token_pad(line,full_tokenizer,subline,n_ctx,token_mask)
                full_line.append(tmp)
                while len(line)>n_ctx:
                    tmp, line = token_pad(line,full_tokenizer,subline,n_ctx,token_mask)
                    full_line.append(tmp)
            else:
                tmp = [full_tokenizer.index('[MASK]')]
                tmp = tmp + subline
                tmp = tmp + [full_tokenizer.index('[CLS]')]
                full_line.extend(tmp)
            if nb_lines%100000==0:
                print('processing file %s with %d lines'%(file,nb_lines))
            if len(full_line)>maxline:
                with open(path_target+str(idx), 'w') as f:
                    f.write('\n'.join(full_line))
                full_line = []
                idx += 1
        f.close()
    with open(path_target + str(idx), 'w') as f:
        f.write('\n'.join(full_line))
    print('finish')
def main(path_vocab,path_source,path_target,token_mask,maxline):
    #tokenizer_path = '../data/vocab/vocab_god_userdata.txt'
    #tokenized_data_path = '../data/userdata_tokenized_new/'
    full_tokenizer = open(path_vocab,'r').read().strip().split('\n')
    build_files(path_source,path_target, full_tokenizer,token_mask,maxline)
    #shutil.rmtree(data_path)
if __name__=='__main__':
    path_vocab,path_source,path_target,token_mask,maxline = sys.argv[1:]
    main(path_vocab,path_source,path_target,token_mask,int(maxline))