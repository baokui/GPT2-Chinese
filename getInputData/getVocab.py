import os
import sys
import json
def getvocab(path_source,files):
    D = {}
    n = 0
    for file in files:
        f = open(os.path.join(path_source,file),'r')
        for line in f:
            d = line.strip()
            for w in d:
                if w in D:
                    D[w] += 1
                else:
                    D[w] = 1
        print(n,len(files),len(D))
        n+=1
    return D
def build_files(data_path, path_target, idx):
    files = os.listdir(data_path)
    F = []
    for file in files:
        if 'part' not in file:
            continue
        if int(file[7:9])!=idx:
            continue
        F.append(file)
    D = getvocab(data_path, F)
    S = [d+'\t'+str(D[d]) for d in D]
    with open(path_target,'w') as f:
        f.write('\n'.join(S))
def getVocab_godText(path_source):
    D = {}
    with open(path_source,'r') as f:
        lines = json.load(f)
    k = 0
    for line in lines:
        for s in line:
            if s in D:
                D[s]+=1
            else:
                D[s] = 1
        if k%100000==0:
            print(k,len(lines),len(D))
    return D
def mergeAll(path_source,path_target,min_nb=1000):
    files = os.listdir(path_source)
    D = {}
    for file in files:
        with open(os.path.join(path_source,file),'r') as f:
            s = f.read().strip().split('\n')
        S = [ss.split('\t') for ss in s]
        for s in S:
            if s[0] not in D:
                D[s[0]] = int(s[-1])
            else:
                D[s[0]] += int(s[-1])
        print(file,len(files),len(D))
    D_god = getVocab_godText(path_source='../data/godText_all1.json')
    for d in D_god:
        if d in D:
            D[d]+=1
        else:
            D[d] = D_god[d]
    T = [(d,D[d]) for d in D]
    T = sorted(T,key=lambda x:-x[-1])
    S = [t[0]+'\t'+str(t[1]) for t in T if t[1]>=0]
    with open(path_target,'w') as f:
        f.write('\n'.join(S))
if __name__=='__main__':
    data_path, path_target, idx = sys.argv[1:4]
    idx = int(idx)
    build_files(data_path, path_target, idx)
