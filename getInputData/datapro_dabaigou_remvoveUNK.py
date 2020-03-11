import os
from collections import Counter
import sys
def remove_unk(idx = 0,unk='100'):
    def count_list(std: list, tongji):
        name = Counter()
        for num in std:
            name[num] += 1
        return name[tongji]
    tokenized_data_path = '../data/dabaigou_tokenized_new/'
    tokenized_data_path1 = '../data/dabaigou_tokenized_new1/'
    files = os.listdir(tokenized_data_path)
    k = 0
    for file in files:
        if k<idx or k>idx+30:
            k += 1
            continue
        f = open(os.path.join(tokenized_data_path,file),'r')
        s = f.read().strip().split()
        f.close()
        R = [s[i*50:(i+1)*50] for i in range(int(len(s)/50))]
        i = 0
        S = []
        for r in R:
            if count_list(r, unk)<2:
                S.extend(r)
            if i%100000==0:
                print('file-{}(total:{}),line-{}(total:{})'.format(k,len(files),int(i/100000),int(len(R)/100000)))
            i += 1
        k += 1
        with open(os.path.join(tokenized_data_path1,file),'w') as f:
            f.write(' '.join(S))
if __name__=='__main__':
    idx = int(sys.argv[1])
    remove_unk(idx)