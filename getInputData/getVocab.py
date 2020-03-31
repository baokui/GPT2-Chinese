import os
import sys
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
if __name__=='__main__':
    data_path, path_target, idx = sys.argv[1:4]
    idx = int(idx)
    build_files(data_path, path_target, idx)
