import json
import numpy as np
import gpt_gen
import gpt_gen_thread
import sys
import time
import torch
from Config import config_predict
path_configs = sys.argv[1].split(',')
path_source,path_target = sys.argv[2:4]
ConfigPredict = config_predict()
ConfigPredict.doPredict[:len(path_configs)] = [True for i in range(len(path_configs))]
ConfigPredict.doPredict[len(path_configs):] = [False for i in range(len(ConfigPredict.doPredict)-len(path_configs))]
ConfigPredict.gpus[:len(path_configs)] = [str(i) for i in range(len(path_configs))]
ConfigPredict.tags[:len(path_configs)] = ['('+str(i)+')' for i in range(len(path_configs))]
batchGenerating=ConfigPredict.batchGenerating
num0 = ConfigPredict.predict_nums
tags = ConfigPredict.tags
rmHFW = ConfigPredict.rmHFW
maxNext = ConfigPredict.maxNext_JLX
path_next = ConfigPredict.path_JLX_next
path_simi = ConfigPredict.path_JLX_simi
model,tokenizer,config,device,GPUs = [],[],[],[],[]
ModelIndex = []
for ii in range(len(path_configs)):
    M0,T0,C0,D0 = [],[],[],[]
    gpus = ConfigPredict.gpus[ii].split(',')
    idx = path_configs[ii].index('config_')+len('config_')
    key = path_configs[ii][idx:-5]
    for gpu in gpus:
        m0,t0,c0,d0 = gpt_gen.getModel(path_config=path_configs[ii],gpu=gpu)
        c0['repetition_penalty'] = ConfigPredict.repetition_penalty[ii]
        c0['temperature'] = ConfigPredict.temperature[ii]
        c0['length'] = ConfigPredict.length[ii]
        M0.append(m0)
        T0.append(t0)
        C0.append(c0)
        D0.append(d0)
    model.append(M0)
    tokenizer.append(T0)
    config.append(C0)
    device.append(D0)
    ModelIndex.append([kk for kk in range(len(gpus))])
    GPUs.append(gpus)
maxModel = len(ConfigPredict.gpus)
if len(model)<maxModel:
    model.extend([[]]*(maxModel-len(model)))
    tokenizer.extend([[]]*(maxModel-len(model)))
    config.extend([[]]*(maxModel-len(model)))
    device.extend([[]]*(maxModel-len(model)))
    ModelIndex.extend([[]]*(maxModel-len(model)))
    GPUs.extend([[]]*(maxModel-len(model)))
D_simi = json.load(open(path_simi,'r',encoding='utf-8'))
D_next = json.load(open(path_next,'r',encoding='utf-8'))
D_simi = {k:json.loads(D_simi[k]) for k in D_simi}
D_next = {k:json.loads(D_next[k]) for k in D_next}
def test(Data):
    modelidx = [np.random.randint(0, len(t)) for t in ModelIndex]
    # gpu_av = GPUtil.getAvailable(order='load', limit=8, maxLoad=0.9, maxMemory=0.9)
    # gpu_av = GPUtil.getAvailable(order='random',maxLoad=0.9, maxMemory=0.9, limit=8)
    # gpu_av = GPUtil.getAvailable(order='memory', limit=8)
    gpu_av = []
    quick = False
    app = ''
    t0 = time.time()
    modl = [model[ii][modelidx[ii]] for ii in range(len(modelidx))]
    conf = [config[ii][modelidx[ii]] for ii in range(len(modelidx))]
    tokn = [tokenizer[ii][modelidx[ii]] for ii in range(len(modelidx))]
    devi = [device[ii][modelidx[ii]] for ii in range(len(modelidx))]
    ConfigPredict.gpus = [GPUs[ii][modelidx[ii]] for ii in range(len(modelidx))]
    R = []
    if ConfigPredict.useThread:
        for D in Data:
            result = gpt_gen_thread.generating_thread(app, D, modl, conf, tokn, devi, ConfigPredict, quick, num0,
                                                      removeHighFreqWordss=rmHFW, batchGenerating=batchGenerating,
                                                      tags=tags,
                                                      D_simi=D_simi, D_next=D_next, maxNext=maxNext, maxChoice=10)
            d = {'input':D,'output':result}
            R.append(d)
    else:
        result = []
        for ii in range(len(path_configs)):
            gpu = ConfigPredict.gpus[ii]
            torch.cuda.set_device(int(gpu))
            if ii == 1:
                r0 = gpt_gen.generating_poem(app, data, model[ii], config[ii], tokenizer[ii], device[ii], quick,
                                             num0[ii], batchGenerating=batchGenerating, gpu=gpu)
            else:
                r0 = gpt_gen.generating(app, data, model[ii], config[ii], tokenizer[ii], device[ii],
                                        ConfigPredict, quick=quick, num=num0[ii], removeHighFreqWords=rmHFW[ii],
                                        batchGenerating=batchGenerating, gpu=gpu)
            r0 = [rr + tags[ii] for rr in r0]
            result.extend(r0)
        result_nnlm = gpt_gen.nnlm_modelpredict(D_simi, D_next, ConfigPredict, inputStr=data, maxNext=maxNext,
                                                maxChoice=10, num=num)
        result += [tmp + tags[-1] for tmp in result_nnlm]
    t1 = time.time()
    print('total inputs:{} and use time: {} s'.format(len(Data), '%0.4f' % (t1 - t0)))
    return R
def main():
    print('test-begin')
    with open(path_source,'r') as f:
        Data = f.read().strip().split('\n')
    t0 = time.time()
    R = test(Data)
    t1 = time.time()
    print('total samples:{},used time:{} s,QPS:{}'.format(len(Data),'%0.4f'%(t1-t0),'%0.4f'%(len(Data)/(t1-t0))))
    with open(path_target,'w') as f:
        json.dump(R,f,ensure_ascii=False,indent=4)
    print('test-over')
if __name__=='__main__':
    main()