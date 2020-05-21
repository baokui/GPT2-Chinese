from modules import *
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
def getdata(path_source='D:\\项目\\输入法\\神配文数据\\淘宝评论\\taobao_comments.txt'):
    with open(path_source,'r',encoding='utf-8') as f:
        s = f.read().strip().split('\n')
    T0 = {}
    T1 = {}
    S = []
    for i in range(len(s)):
        t = s[i].split('\t')
        if t[0] in T0:
            T0[t[0]].append(t[-1])
        else:
            T0[t[0]] = [t[-1]]
        if t[1] in T1:
            T1[t[1]].append(t[-1])
        else:
            T1[t[1]] = [t[-1]]
        S.append(t[-1])
    Len = [len(t) for t in S]
    A = set(Len)
    B = []
    for a in A:
        B.append([a,sum([t==a for t in Len])])
    B = sorted(B,key=lambda x:x[0])
    C = [[b[0],b[1]/len(S)] for b in B]
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
    V = getVocab(S0)
    V = [v[0] for v in V if v[1]>=100]
    V = VocabExtend(V)
    with open('comments/data/vocab.txt','w',encoding='utf-8') as f:
        f.write('\n'.join(V))
    T = []
    for s in S0:
        t = tokenization(s,V)
        if t:
            T.append(t)
    T = [[str(tt) for tt in t] for t in T]
    T = [' '.join(t) for t in T]
    with open('comments/tokens/token1.txt','w') as f:
        f.write('\n'.join(T))