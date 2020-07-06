import os
import numpy as np
import random
minlen = 10
maxlen = 64
path_source = 'D:\\项目\\输入法\\神配文数据\\评论\\抖音皮皮虾\\data1'
path_target = 'D:\\项目\\输入法\\神配文数据\\评论\\抖音皮皮虾\\model'
path_tokens = 'D:\\项目\\输入法\\神配文数据\\评论\\抖音皮皮虾\\tokens'
files = os.listdir(path_source)
files = [os.path.join(path_source,file) for file in files]
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
def check(s1):
    if len(s1)<minlen:
        return False
    if s1[0]=='@' and len(s1.strip().split())==1:
        return False
    f = [_is_chinese_char(ss) for ss in s1]
    if sum(f)<0.7*len(s1):
        return False
    return True
S0 = []
for file in files:
    with open(file,'r',encoding='utf-8') as f:
        D = f.read().strip().split('\n')
    if 'zhihu' in file:
        S0.extend([d.split('\t')[-1] for d in D])
    else:
        S0.extend([d.split('\t')[0] for d in D])
S = []
for s in S0:
    if check(s):
        S.append(s)

V = {}
for s in S:
    for aa in s:
        if aa not in V:
            V[aa] = 1
        else:
            V[aa]+=1
V = [[d,V[d]] for d in V]
V = sorted(V,key=lambda x:-x[-1])
V = [v for v in V if v[-1]>=4]
V = [v[0] for v in V]
V0 = ['[MASK]','[PAD]','[UNK]','[CLS]']
V1 = ['unused'+str(i) for i in range(100)]
V = V0+V+V1
with open(os.path.join(path_target,'vocab.txt'),'w',encoding='utf-8') as f:
    f.write('\n'.join(V))

def tokenization(s):
    r = [V.index('[MASK_gou]')]
    for t in s:
        if t not in V:
            r.append(V.index('[UNK]'))
        else:
            r.append(V.index(t))
    if len(r)<maxlen-1:
        r.extend([V.index('[PAD]') for _ in range(maxlen-1-len(r))])
    r = r[:maxlen-1]
    r.append(V.index('[CLS]'))
    return r
TT = []
for t in S:
    s = tokenization(t)
    s = [str(ss) for ss in s]
    d = ' '.join(s)
    TT.append(d)
    if len(TT)%1000==0:
        print(len(TT),len(S))
with open(os.path.join(path_tokens,'token.txt'),'w',encoding='utf-8') as f:
    f.write('\n'.join(TT))