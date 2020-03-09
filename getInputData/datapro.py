import sys
import os
import shutil
import tqdm
from tokenizations import tokenization_bert
import random
def build_files(data_path, dataname, tokenized_data_path, full_tokenizer,n_ctx = 1024, min_length=15,num_pieces=1, max_nb = 10000000):
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

def main(data_path,dataname):
    tokenizer_path = '../model/gpt2_prose/vocab.txt'
    tokenized_data_path = '../data/dabaigou_tokenized/'
    full_tokenizer = tokenization_bert.BertTokenizer(vocab_file=tokenizer_path)
    build_files(data_path, dataname, tokenized_data_path, full_tokenizer)
    shutil.rmtree(data_path)
if __name__=='__main__':
    data_path,dataname = sys.argv[1:3]
    main(data_path,dataname)