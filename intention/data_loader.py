import json
import random
import os
def read_vocab():
    pass
def read_category():
    pass
def batch_iter(path_data,tokenizer,max_len=10,batch_size=64,epochs = 1):
    x = []
    y = []
    for epoch in range(epochs):
        f = open(path_data, 'r')
        for line in f:
            s = line.strip().split('\t')
            if len(s)!=2:
                continue
            t = tokenizer.tokenization(s[0],max_len=max_len)
            x.append(t)
            z = int(s[1])
            if z==0:
                y.append([0,1])
            else:
                y.append([1,0])
            if len(x)==batch_size:
                yield epoch,x,y
                x = []
                y = []
        f.close()
    yield '__STOP__'
def batch_iter_test(path_data,tokenizer,max_len=10,batch_size=10000):
    x = []
    y = []
    while True:
        f = open(path_data, 'r')
        for line in f:
            s = line.strip().split('\t')
            if len(s)!=2:
                continue
            t = tokenizer.tokenization(s[0],max_len=max_len)
            x.append(t)
            z = int(s[1])
            if z==0:
                y.append([0,1])
            else:
                y.append([1,0])
            if len(x)==batch_size:
                yield x,y
                x = []
                y = []
        f.close()
def process_file():
    pass
def build_vocab():
    pass
def build_dataset(path_pos,path_neg,nb_test_pos = 100000,nb_test_neg = 100000,min_len=2,max_len=10):
    with open(path_pos,'r') as f:
        s = json.load(f)
    random.shuffle(s)
    x_pos = []
    for i in range(nb_test_pos,len(s)):
        L = random.randint(min_len,max_len)
        x_pos.append(s[i][:L])
    x_test_pos = []
    for i in range(nb_test_pos):
        L = random.randint(min_len,max_len)
        x_test_pos.append(s[i][:L])
    files = os.listdir(path_neg)
    files = [os.path.join(path_neg,file,'part-00001') for file in files]
    nb_neg_each = int(len(x_pos)/len(files))
    nb_test_neg_each = int(nb_test_neg/len(files))
    x_neg = []
    x_test_neg = []
    for file in files:
        print(file)
        f = open(file,'r')
        x0 = []
        x1 = []
        for line in f:
            t = line.strip().split('\t')[1]
            L = random.randint(min_len, max_len)
            t = t[:L]
            if len(x0)<nb_neg_each:
                x0.append(t)
                continue
            if len(x1)<nb_test_neg_each:
                x1.append(t)
                continue
            if len(x0)==nb_neg_each and len(x1)==nb_test_neg_each:
                break
        x_neg.extend(x0)
        x_test_neg.extend(x1)
    STrn = [t.replace('\t','')+'\t'+'1' for t in x_pos]
    STrn += [t.replace('\t','')+'\t'+'0' for t in x_neg]
    STst = [t.replace('\t','')+'\t'+'1' for t in x_test_pos]
    STst += [t.replace('\t','')+'\t'+'0' for t in x_test_neg]
    random.shuffle(STrn)
    with open('data/train.txt','w') as f:
        f.write('\n'.join(STrn))
    random.shuffle(STst)
    with open('data/test.txt','w') as f:
        f.write('\n'.join(STst))
    D = {}
    x = x_pos+x_neg
    for i in range(len(x)):
        for j in range(len(x[i])):
            if x[i][j] in D:
                D[x[i][j]]+=1
            else:
                D[x[i][j]]=1
        if i%10000==0:
            print(i,i/len(x))
    T = [(d,D[d]) for d in D]
    T = sorted(T,key=lambda x:-x[-1])
    T = [t[0] for t in T]
    with open('data/vocab.txt','w') as f:
        f.write('\n'.join(T))