import json
from peomGenerator import peomSplit
import sys
def getStats(path_source):
    with open(path_source, 'r') as f:
        data = json.load(f)
    n = 5
    N = len(data)
    N_all = 0
    N_less5_head = 0
    N_less5_sent = 0
    A = []
    for i in range(N):
        if i%100000==0:
            print('number of all/head less than 5 chars/sent less than 5 chars is %d/%d/%d'%(N,N_less5_head,N_less5_sent))
            print(A)
        S = peomSplit(data[i])
        N_all+=len(S)
        if len(S[0])<n:
            N_less5_head += 1
            A.append(data[i])
        for s in S:
            if len(s)<n:
                N_less5_sent += 1
    print('number of all/head less than 5 chars/sent less than 5 chars is %d/%d/%d' % (N, N_less5_head, N_less5_sent))
    print('全部诗词：%d'%N)
    print('全部诗词的诗句：%d'%N_all)
    print('少于5个字的诗句：%d'%N_less5_sent)
    print('少于5个字的首句：%d'%N_less5_head)
    with open('data/p_small.json','w') as f:
        json.dump(A,f,ensure_ascii=False,indent=4)
def poemMerge():
    import os
    import json
    path_target = 'poem_generate/all.txt'
    files = os.listdir('data')
    N = 0
    for i in range(len(files)):
        with open('data/'+files[i],'r') as f:
            s = f.read().strip().split('\n')
        S = s
        with open(path_target, 'a+') as f:
            f.write('\n'.join(S) + '\n')
        N += len(S)
        if i%100==0:
            print(i,len(files),N)
    files = os.listdir('data45')
    for i in range(len(files)):
        with open('data45/' + files[i], 'r') as f:
            s = f.read().strip().split('\n')
        S = s
        with open(path_target, 'a+') as f:
            f.write('\n'.join(S) + '\n')
        N += len(S)
        if i % 100 == 0:
            print(i, len(files), N)
def selectPoem():
    path_source = 'poem_generate/all.txt'
    path_target = 'poem_generate/all_5.txt'
    num = 5
    lastkey = '**'
    f = open(path_source,'r')
    f_w = open(path_target, 'a+')
    S = []
    R = []
    n = 0
    for line in f:
        if '□' in line:
            continue
        fields = line.strip().split('\t')
        if len(fields)!=2:
            continue
        key,value = fields
        if value[0] in '。？！':
            continue
        if len(value)<3*len(key)+4:
            continue
        if key!=lastkey:
            if lastkey!='**':
                S = S[:num]
                A = [lastkey+ss for ss in S]
                R.extend(A)
                _ = f_w.write('\n'.join(A) + '\n')
            lastkey = key
            S = []
        S.append(value)
        if n%10000==0:
            print(n,len(R))
        n+=1
    S = S[:num]
    A = [lastkey + ss for ss in S]
    R.extend(A)
    _ = f_w.write('\n'.join(A) + '\n')
    R1 = sorted(R)

    def _is_chinese_char(char):
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

    R11 = []
    R12 = []
    for r in R1:
        if _is_chinese_char(r[0]):
            R11.append(r)
        else:
            R12.append(r)
    with open('poem_generate/generate.txt','w') as f:
        f.write('\n'.join(R11))
if __name__=='__main__':
    path_sourc = sys.argv[1]
    getStats(path_sourc)