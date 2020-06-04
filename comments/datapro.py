import random
import os
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
def VocabExtend(V,nb_unused=100):
    V0 = ['[PAD]', '[UNK]', '[CLS]', '[SEP]', '[MASK]', '<S>', '<T>']
    V1 = ['unused'+str(i) for i in range(nb_unused)]
    Vn = V0+[v for v in V]+V1
    return Vn
def getVocab(S):
    D = {}
    for i in range(len(S)):
        for j in range(len(S[i])):
            if S[i][j] not in D:
                D[S[i][j]] = 1
            else:
                D[S[i][j]] += 1
    T = [(d,D[d]) for d in D]
    T = sorted(T,key=lambda x:-x[-1])
    return T
def tokenization(S,vocab,padding=True,n_ctx = 64,min_len=8,punc_end='，。？！'):
    if len(S)>n_ctx-2:
        S = S[:n_ctx-2]
        for i in range(len(S)):
            if S[len(S)-i-1] in punc_end:
                S = S[:len(S)-i]
                break
    if len(S)<min_len:
        return []
    T0 = [vocab.index('[MASK]')]
    T2 = [vocab.index('[CLS]')]
    token_unk = vocab.index('[UNK]')
    T1 = []
    nb_unk = 0
    for i in range(len(S)):
        if S[i] in vocab:
            T1.append(vocab.index(S[i]))
        else:
            T1.append(token_unk)
            nb_unk+=1
    if nb_unk>2:
        return []
    T = T0+T1
    if len(T)<n_ctx-1:
        T = T+[vocab.index('[PAD]') for _ in range(n_ctx-1-len(T))]
    T = T+T2
    return T
def getdata(path_source0='D:\\项目\\输入法\\神配文数据\\淘宝评论\\data'):
    files = os.listdir(path_source0)
    files = [os.path.join(path_source0,file) for file in files]
    S00 = []
    for path_source in files:
        with open(path_source,'r',encoding='utf-8') as f:
            s = f.read().strip().split('\n')
        S = []
        for i in range(len(s)):
            t = s[i].split('\t')
            if len(t)<5:
                continue
            S.append(t[4])
        S0 = []
        S1 = []
        min_nb_zh = 8
        min_rate_zh = 0.6
        for i in range(len(S)):
            s = S[i]
            t = [_is_chinese_char(ss) for ss in s]
            nb_zh = sum(t)
            rate_zh = sum(t)/len(t)
            if nb_zh<min_nb_zh or rate_zh<min_rate_zh:
                S1.append(s)
            else:
                S0.append(s)
        print(path_source)
        print(len(S0))
        print(S0[:3])
        S00.extend(S0)
    V = getVocab(S00)
    V1 = [v[0] for v in V if v[1]>=100]
    V1 = VocabExtend(V1)
    with open('data/vocab_addpdd.txt','w',encoding='utf-8') as f:
        f.write('\n'.join(V1))

    random.shuffle(S00)
    with open('comments/data/comments_all_addpdd.txt','w',encoding='utf-8') as f:
        f.write('\n'.join(S00))
    T = []
    for s in S00:
        t = tokenization(s,V1)
        if t:
            T.append(t)
        if len(T)%10000==0:
            print(len(T),len(T)/len(S00))
    #T = [[str(tt) for tt in t] for t in T]
    #T = [' '.join(t) for t in T]
    i = 0
    N = 100000
    i0 = i*N
    i1 = (i+1)*N
    while i0<len(T):
        print(i)
        s = T[i0:i1]
        s = [[str(tt) for tt in t] for t in s]
        s = [' '.join(t) for t in s]
        with open('comments/tokens_addpdd/token'+str(i)+'.txt','w') as f:
            f.write('\n'.join(s))
        i+=1
        i0 = i * N
        i1 = (i + 1) * N
