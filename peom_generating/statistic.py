import json
from peomGenerator import peomSplit
import sys
def getStats(path_source):
    with open(path_source, 'r') as f:
        data = json.load(f)
    n = 5
    N = len(data)
    N_less5_head = 0
    N_less5_sent = 0
    for i in range(N):
        if i%10000==0:
            print('number of all/head less than 5 chars/sent less than 5 chars is %d/%d/%d'%(N,N_less5_head,N_less5_sent))
        S = peomSplit(data[i])
        if len(S[0])<n:
            N_less5_head += 1
        for s in S:
            if len(s)<n:
                N_less5_sent += 1
    print('number of all/head less than 5 chars/sent less than 5 chars is %d/%d/%d' % (N, N_less5_head, N_less5_sent))
    print('全部诗词：%d'%N)
    print('少于5个字的诗句：%d'%N_less5_sent)
    print('少于5个字的首句：%d'%N_less5_head)
    
if __name__=='__main__':
    path_sourc = sys.argv[1]
    getStats(path_sourc)