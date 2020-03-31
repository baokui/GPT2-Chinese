import os
def getvocab(path_source):
    D = {}
    files = os.listdir(path_source)
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
