import os
import random
import sys
def iterData(path0,batch_size=5000000,n_ctx=64):
    files = os.listdir(path0)
    S = []
    for file in files:
        f = open(os.path.join(path0,file),'r')
        s = f.read().strip().split()
        t = [s[i*n_ctx:(i+1)*n_ctx] for i in range(int(len(s)/n_ctx))]
        S.extend(t)
        while len(S)>batch_size:
            yield S[:batch_size]
            S = S[batch_size:]
        f.close()
    if len(S)>0:
        yield S
    yield '__STOP__'
def pro(path_gou,path_godText,path_target,r=0.5):
    b0 = int(1000000*r)
    b1 = 1000000-b0
    iter_gou = iterData(path_gou,b0)
    iter_godText = iterData(path_godText,b1)
    s0 = next(iter_gou)
    s1 = next(iter_godText)
    idx = 0
    N = 0
    while s0!='__STOP__':
        if s1=='__STOP__':
            iter_godText = iterData(path_godText, b1)
            s1 = next(iter_godText)
        s = s0+s1
        N+=len(s)
        random.shuffle(s)
        t = []
        for ss in s:
            t.extend(ss)
        with open(os.path.join(path_target,'file-'+str(idx)+'.txt'),'w') as f:
            f.write(' '.join(t))
        print('get {} samples and {} files'.format(N,idx+1))
        idx+=1
        s0 = next(iter_gou)
        s1 = next(iter_godText)

if __name__=='__main__':
    path_gou, path_godText, path_target = sys.argv[1:]
    pro(path_gou,path_godText,path_target)