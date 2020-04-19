# -*- encoding: utf-8 -*-
from flask import Flask, request, Response
import json
import torch
import numpy as np
import gpt_gen
import gpt_gen_thread
import sys
from datetime import datetime
import time
import logging
from Config import config_predict

path_source = sys.argv[1]
path_target = sys.argv[2]
if len(sys.argv)>3:
    path_config = sys.argv[3].split(',')
    doPredict = [int(t) for t in sys.argv[4].split(',')]
    gpus = sys.argv[5].split(',')
    ConfigPredict = config_predict(model_config=path_config,doPredict=doPredict,gpus = gpus)
    print('use input configs:%s'%'\n'.join(path_config))
    print('gpus=%s'%','.join(ConfigPredict.gpus))
else:
    print('use default configs')
    ConfigPredict = config_predict()
with open(path_source,'r') as f:
    Data = f.read().strip().split('\n')
batchGenerating=ConfigPredict.batchGenerating
path_configs = ConfigPredict.model_configs
num0 = ConfigPredict.predict_nums
tags = ConfigPredict.tags
rmHFW = ConfigPredict.rmHFW
maxNext = ConfigPredict.maxNext_JLX
path_next = ConfigPredict.path_JLX_next
path_simi = ConfigPredict.path_JLX_simi
model,tokenizer,config,device = [], [], [], []
for ii in range(len(path_configs)):
    if ConfigPredict.doPredict[ii]:
        m0,t0,c0,d0 = gpt_gen.getModel(path_config=path_configs[ii],gpu=ConfigPredict.gpus[ii])
        c0['repetition_penalty'] = ConfigPredict.repetition_penalty[ii]
        c0['temperature'] = ConfigPredict.temperature[ii]
        c0['length'] = ConfigPredict.length[ii]
    else:
        m0,t0,c0,d0 = '','','',''
    model.append(m0)
    tokenizer.append(t0)
    config.append(c0)
    device.append(d0)
if ConfigPredict.doPredict[-1]:
    D_simi = json.load(open(path_simi,'r',encoding='utf-8'))
    D_next = json.load(open(path_next,'r',encoding='utf-8'))
    D_simi = {k:json.loads(D_simi[k]) for k in D_simi}
    D_next = {k:json.loads(D_next[k]) for k in D_next}
else:
    D_simi,D_next = [],[]
app = 0
quick = False
def write_excel(path_target,data,sheetname='Sheet1'):
    import xlwt
    # 创建一个workbook 设置编码
    workbook = xlwt.Workbook(encoding='utf-8')
    # 创建一个worksheet
    worksheet = workbook.add_sheet(sheetname)
    # 写入excel
    # 参数对应 行, 列, 值
    rows,cols = len(data),len(data[0])
    for i in range(rows):
        for j in range(cols):
            worksheet.write(i, j, label=str(data[i][j]))
    # 保存
    workbook.save(path_target)
def main():
    S = []
    T0 = time.time()
    for data in Data:
        if ConfigPredict.useThread:
            result = gpt_gen_thread.generating_thread(app, data, model, config, tokenizer, device, ConfigPredict,quick, num0,
                                                       removeHighFreqWordss=rmHFW, batchGenerating=batchGenerating,tags=tags,
                                                      D_simi=D_simi,D_next=D_next,maxNext=maxNext,maxChoice=10)
        else:
            result = []
            for ii in range(len(path_configs)):
                gpu = ConfigPredict.gpus[ii]
                torch.cuda.set_device(int(gpu))
                if ii==1:
                    r0 = gpt_gen.generating_poem(app,data, model[ii], config[ii], tokenizer[ii],device[ii],quick,num0[ii],batchGenerating=batchGenerating,gpu=gpu)
                else:
                    r0 = gpt_gen.generating(app,data, model[ii], config[ii], tokenizer[ii],device[ii],ConfigPredict,quick=quick,num=num0[ii],removeHighFreqWords=rmHFW[ii],batchGenerating=batchGenerating,gpu=gpu)
                r0 = [rr + tags[ii] for rr in r0]
                result.extend(r0)
            result_nnlm = gpt_gen.nnlm_modelpredict(D_simi,D_next,ConfigPredict,inputStr=data,maxNext=maxNext,maxChoice=10,num=num)
            result += [tmp+tags[-1] for tmp in result_nnlm]
        response = {'input':data,'result': result}
        S.append(response)
    T1 = time.time()
    T = T1 - T0
    with open(path_target, 'w') as f:
        json.dump(S, f, ensure_ascii=False, indent=4)
    A = []
    for i in range(len(S)):
        for j in range(len(S[i]['result'])):
            s = S[i]['result'][j]
            t = ''.join([s[len(s) - i - 1] for i in range(len(s))])
            idx0 = len(s) - t.find('(') - 1
            idx1 = len(s) - t.find(')') - 1
            tag = s[idx0:idx1 + 1]
            if j == 0:
                z = [S[i]['input'], S[i]['result'][j]]
            else:
                z = ['', S[i]['result'][j]]
            z.append(tag)
            A.append(z)
    path_target1 = path_target.replace('json', 'xls')
    write_excel(path_target1, A)
    print('used time %0.2f and QPS=%0.2f' % (T, len(Data) / T))
# start flask app
if __name__ == '__main__':
    main()
