import time
import os
import sys
def tokenFilter(path_source,path_target,nb_min=8):
    #f = open(path_source,'r')
    #with open(path_source,'r') as f:
        #s = f.read().strip()
    #s = s.split()
    f = open(path_source,'r')
    T = []
    N = 0
    for line in f:
        s = line.strip().split()
        N+=len(s)
        nb = 0
        i0 = 0
        i1 = i0+1
        while i1<len(s):
            while s[i1]!='2':
                if s[i1]!='0':
                    nb+=1
                i1+=1
            if nb>nb_min:
                T.extend(s[i0:i1+1])
            nb=0
            i0 = i1+1
            i1 = i1+1
            if len(T)%6400000==0:
                print(len(T)/64,N/64)
    T = ' '.join(T)
    with open(path_target,'w') as f:
        f.write(T)
def main(path_source0,path_target0):
    tokenFilter(path_source0,path_target0)
if __name__=='__main__':
    path_source,path_target = sys.argv[1:3]
    main(path_source,path_target)
