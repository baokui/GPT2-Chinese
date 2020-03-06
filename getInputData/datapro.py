import sys
import os
from tokenizations import tokenization_bert
def build_files(data_path, dataname, tokenized_data_path, full_tokenizer, min_length=10,num_pieces=1, max_nb = 10000000):
    if not os.path.exists(tokenized_data_path):
        os.mkdir(tokenized_data_path)
    k = 0
    for ii in range(5):
        lines = []
        f = open(data_path+'/part-0000'+str(ii), 'r', encoding='utf8')
        print('reading lines')
        for line in f:
            lines.append(line.replace('\n', ' [SEP] '))  # 用[SEP]表示换行, 段落之间使用SEP表示段落结束
            if len(lines)<max_nb:
                continue
            if len(lines)%1000==0:
                print('processing file %s, %d, %0.2f'%(data_path,len(lines),len(lines)/float(max_nb)))
            all_len = len(lines)
            for i in range(num_pieces):
                sublines = lines[all_len // num_pieces * i: all_len // num_pieces * (i + 1)]
                if i == num_pieces - 1:
                    sublines.extend(lines[all_len // num_pieces * (i + 1):])  # 把尾部例子添加到最后一个piece
                sublines = [full_tokenizer.tokenize(line) for line in sublines if
                            len(line) > min_length]  # 只考虑长度超过min_length的句子
                sublines = [full_tokenizer.convert_tokens_to_ids(line) for line in sublines]
                full_line = []
                for subline in sublines:
                    full_line.append(full_tokenizer.convert_tokens_to_ids('[MASK]'))  # 文章开头添加MASK表示文章开始
                    full_line.extend(subline)
                    full_line.append(full_tokenizer.convert_tokens_to_ids('[CLS]'))  # 文章之间添加CLS表示文章结束
                with open(tokenized_data_path + dataname+'.txt'.format(k), 'w') as f:
                    for id in full_line:
                        f.write(str(id) + ' ')
                k += 1
                lines = []
        f.close()
    print('finish')
def main(data_path,dataname):
    tokenizer_path = '../model/gpt2_prose/vocab.txt'
    tokenized_data_path = '../data/sogouInput_tokenized/'
    full_tokenizer = tokenization_bert.BertTokenizer(vocab_file=tokenizer_path)
    build_files(data_path, dataname, tokenized_data_path, full_tokenizer)
    os.remove(data_path)
if __name__=='__main__':
    data_path,dataname = sys.argv[1:3]
    main(data_path,dataname)