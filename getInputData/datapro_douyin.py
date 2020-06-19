import os
import numpy as np
import random
minlen = 6
path_source = 'D:\\项目\\输入法\\神配文数据\\评论\\抖音皮皮虾\\data'
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
S = []
M = []
for file in files:
    with open(file,'r',encoding='utf-8') as f:
        D = f.read().strip().split('\n')
    D = [d.split('\t') for d in D]
    N = sum([int(d[-1]) for d in D])
    D = [[d[0],np.log((int(d[-1])+1)/N)] for d in D]
    M.extend([d[-1] for d in D])
    D = ['\t'.join([d[0],'%0.4f'%d[1]]) for d in D]
    S.extend(D)
    print(N,len(D),D[0])
    for s in D:
        if '@' in s[0]:
            print(s)
            break

m0 = min(M)
m1 = max(M)
m0 = m0-0.1
m1 = m1+0.1
S = [s.split('\t') for s in S]
S = [[s[0],(float(s[1])-m0)/(m1-m0)] for s in S]
S = [[s[0],'%0.4f'%s[1]] for s in S]

T = []
for s in S:
    tmp = s[0]
    if '@' in s[0]:
        z = s[0].split()
        for zz in z:
            if zz[0]=='@':
                tmp = tmp.replace(zz,'')
    n = sum([_is_chinese_char(tt) for tt in tmp])
    if n<minlen:
        continue
    T.append(tmp+'\t'+s[1])
random.shuffle(T)
with open(os.path.join(path_target,'data.txt'),'w',encoding='utf-8') as f:
    f.write('\n'.join(T))
V = {}
for t in T:
    a = t.split('\t')[0]
    for aa in a:
        if aa not in V:
            V[aa] = 1
        else:
            V[aa]+=1
V = [[d,V[d]] for d in V]
V = sorted(V,key=lambda x:-x[-1])
V = [v for v in V if v[-1]>=5]
V = [v[0] for v in V]
V0 = ['[MASK]','[PAD]','[UNK]','[CLS]']+['unused'+str(i) for i in range(20)]
V = V0+V
with open(os.path.join(path_target,'vocab.txt'),'w',encoding='utf-8') as f:
    f.write('\n'.join(V))

maxlen = 60
def tokenization(s):
    r = [V.index('[MASK]')]
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
for t in T:
    a = t.split('\t')
    p = a[1]
    s = tokenization(a[0])
    s = [str(ss) for ss in s]
    d = p+'\t'+' '.join(s)
    TT.append(d)
    if len(TT)%1000==0:
        print(len(TT),len(T))
with open(os.path.join(path_tokens,'token.txt'),'w',encoding='utf-8') as f:
    f.write('\n'.join(TT))