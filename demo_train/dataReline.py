import os
def fun(path_source,path_target,n_ctx=64,n=100):
    with open(path_source,'r') as f:
        s = f.read().strip().split()
    tokens = s
    tokens = tokens[tokens.index('4'):]
    tokens = tokens[:int(len(tokens) / n_ctx) * n_ctx]
    T = []
    i=0
    while i* n_ctx*n<len(tokens):
        t = tokens[i * n_ctx*n:(i + 1) * n_ctx*n]
        T.append(' '.join(t))
        i+=1
    S = '\n'.join(T)
    with open(path_target,'w') as f:
        f.write(S)
def main(path_source0):
    files = os.listdir(path_source0)
    for i in range(len(files)):
        path_source = os.path.join(path_source0,files[i])
        path_target = path_source
        fun(path_source, path_target)
        print('proceed-{}(total {})'.format(i,len(files)))
if __name__=='__main__':
    main('data_vpa_dialogue1')

