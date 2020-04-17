import sys
import os
import json
from tokenizations import tokenization_bert
def _is_chinese_char(char):
    """Checks whether CP is the codepoint of a CJK character."""
    # This defines a "chinese character" as anything in the CJK Unicode block:
    #   https://en.wikipedia.org/wiki/CJK_Unified_Ideographs_(Unicode_block)
    #
    # Note that the CJK Unicode block is NOT all Japanese and Korean characters,
    # despite its name. The modern Korean Hangul alphabet is a different block,
    # as is Japanese Hiragana and Katakana. Those alphabets are used to write
    # space-separated words, so they are not treated specially and handled
    # like the all of the other languages.
    cp = ord(char)
    if ((cp >= 0x4E00 and cp <= 0x9FFF) or  #
            (cp >= 0x3400 and cp <= 0x4DBF) or  #
            (cp >= 0x20000 and cp <= 0x2A6DF) or  #
            (cp >= 0x2A700 and cp <= 0x2B73F) or  #
            (cp >= 0x2B740 and cp <= 0x2B81F) or  #
            (cp >= 0x2B820 and cp <= 0x2CEAF) or
            (cp >= 0xF900 and cp <= 0xFAFF) or  #
            (cp >= 0x2F800 and cp <= 0x2FA1F)):  #
        return True

    return False
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
def build_files(full_tokenizer,path_source,path_target,padding,n_ctx=64,min_length=6,maxNb=1000000):
    if not os.path.exists(path_target):
        os.mkdir(path_target)
    full_line = []
    print('reading lines')
    nb_lines = 0
    files = os.listdir(path_source)
    idx = 0
    for file in files:
        f = open(os.path.join(path_source,file),'r')
        for line in f:
            line_zh = [tt for tt in line if _is_chinese_char(tt)]
            if len(line_zh)<min_length or len(line)>len(line_zh)*2:
                continue
            nb_lines+=1
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
                print('processing file %s and get %d lines'%(file,nb_lines))
            if nb_lines>=maxNb:
                nb_lines = 0
                with open(os.path.join(path_target, 'godTokenizer_' + str(idx) + '.txt'), 'w') as f:
                    f.write(' '.join(full_line))
                idx+=1
                full_line = []
    if len(full_line)>0:
        with open(os.path.join(path_target, 'godTokenizer_' + str(idx) + '.txt'), 'w') as f:
            f.write(' '.join(full_line))
    print('finish')
def main(path_source,path_target,padding,path_vocab,n_ctx):
    #tokenizer_path = '../data/vocab/vocab_god_userdata.txt'
    #tokenized_data_path = '../data/userdata_tokenized_new/'
    full_tokenizer = tokenization_bert.BertTokenizer(vocab_file=path_vocab)
    build_files(full_tokenizer,path_source,path_target,padding,n_ctx=n_ctx)
    #shutil.rmtree(data_path)
if __name__=='__main__':
    path_source,path_target,padding,path_vocab,n_ctx = sys.argv[1:6]
    padding = padding=='1'
    main(path_source,path_target,padding,path_vocab,int(n_ctx))