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
if __name__=="__main__":
    mode = sys.argv[1]
    if mode=='segment':
        path_source,path_target = sys.argv[2:4]
        segment(path_source,path_target)