import jieba_fast as jieba
import os
import sys
def segment(path_source,path_target):
    files = os.listdir(path_source)
    n = 0
    f_w = open(path_target,'w')
    S = []
    for file in files:
        if 'part' not in file:
            continue
        f = open(os.path.join(path_source,file),'r')
        for line in f:
            data = line.strip().split('\t')
            if len(data)!=2:
                continue
            sent = ' '.join(list(jieba.cut(data[1].lower())))
            n+=1
            S.append('\t'.join([data[0],sent])+'\n')
            if n%100000==0:
                f_w.write(''.join(S))
                S = []
                print('sengment file %s with %d lines'%(file,n))
    if len(S)>0:
        f_w.write(''.join(S))
def getVocab(path_source,path_target,filname,max_line=10000000):
    if not os.path.exists(path_target):
        os.mkdir(path_target)
    f = open(path_source,'r')
    N = 0
    n = -1
    D = {}
    S = []
    for line in f:
        n += 1
        data = line.strip().split('\t')
        if len(data)!=2:
            continue
        s = data[1].split(' ')
        for ss in s:
            if ss not in D:
                D[ss] = 1
            else:
                D[ss] += 1
        if n>0 and n%max_line==0:
            S = [[k,str(D[k])] for k in D]
            S = sorted(S,key=lambda x:x[0])
            S = ['\t'.join(tmp) for tmp in S]
            with open(os.path.join(path_target,filname+'_'+str(N)+'.txt'),'w') as f_w:
                f_w.write('\n'.join(S))
            print('complete %d lines for %s'%(n,path_source))
            N += 1
            D = {}

    if len(S)>0:
        with open(os.path.join(path_target, filname + '_' + str(N) + '.txt'), 'w') as f_w:
            f_w.write('\n'.join(S))
    f.close()
if __name__=="__main__":
    mode = sys.argv[1]
    if mode=='segment':
        path_source,path_target = sys.argv[2:4]
        segment(path_source,path_target)
    if mode=='vocab':
        path_source, path_target,filename = sys.argv[2:5]
        getVocab(path_source,path_target,filename)