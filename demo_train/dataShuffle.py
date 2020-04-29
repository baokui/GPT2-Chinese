import random
import os
def getdata(path_source,path_target,rate_data=0.01):
    f = open(path_source,'r')
    S = []
    for line in f:
        if random.uniform(0,1)>rate_data:
            continue
        S.append(line)
    with open(path_target,'w') as f:
        f.write('\n'.join(S))
def main(path_data):
    pass