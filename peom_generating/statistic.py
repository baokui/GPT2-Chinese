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
if __name__=='__main__':
    path_sourc = sys.argv[1]
    getStats(path_sourc)