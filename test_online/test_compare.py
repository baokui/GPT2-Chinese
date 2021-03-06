from flask import Flask, request, Response
import json
import numpy as np
import gpt_gen
import gpt_gen_thread
import sys
import time
import logging
import torch
from Config import config_predict
from datetime import datetime
ConfigPredict = config_predict()
batchGenerating=ConfigPredict.batchGenerating
path_configs = ConfigPredict.model_configs
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
D_simi = json.load(open(path_simi,'r',encoding='utf-8'))
D_next = json.load(open(path_next,'r',encoding='utf-8'))
D_simi = {k:json.loads(D_simi[k]) for k in D_simi}
D_next = {k:json.loads(D_next[k]) for k in D_next}
def read_excel(path_source1,index=0):
    import xlrd
    workbook = xlrd.open_workbook(path_source1)  # 打开excel文件
    sheets = workbook.sheets()
    table = workbook.sheet_by_name(sheets[index].name)  # 将文件内容表格化
    rows_num = table.nrows  # 获取行
    cols_num = table.ncols  # 获取列
    res = []  # 定义一个数组
    for rows in range(rows_num):
        r = []
        for cols in range(cols_num):
            r.append(table.cell(rows, cols).value)  # 获取excel中单元格的内容
        res.append(r)
    return res
def getdata(path_data='D:\项目\输入法\神配文数据\生成评测\主动详情准确率3.xlsx',path_targe='test_online/data/test_0416.json'):
    data = read_excel(path_data,index=0)
    D = []
    prefix = ''
    r = []
    for i in range(1,len(data)):
        if data[i][0]!='':
            if prefix!='':
                d = {'input':prefix,'ouput':r}
                D.append(d)
            prefix = data[i][0]
            r = []
        if data[i][4]==0 or data[i][4]==1 or data[i][4]==2:
            r.append(data[i][3]+'\t'+str(int(data[i][4])))
    if prefix!='':
        d = {'input':prefix,'ouput':r}
        D.append(d)
    with open(path_targe,'w',encoding='utf-8') as f:
        json.dump(D,f,ensure_ascii=False,indent=4)
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
def test(Data,sym='-new'):
    modelidx = [np.random.randint(0, len(t)) for t in ModelIndex]
    # gpu_av = GPUtil.getAvailable(order='load', limit=8, maxLoad=0.9, maxMemory=0.9)
    # gpu_av = GPUtil.getAvailable(order='random',maxLoad=0.9, maxMemory=0.9, limit=8)
    # gpu_av = GPUtil.getAvailable(order='memory', limit=8)
    gpu_av = []
    gpu_opt = 0
    if len(gpu_av) > 0:
        for i in range(len(gpu_av)):
            for j in range(len(GPUs)):
                if str(gpu_av[i]) in GPUs[j]:
                    gpu_opt = 1
                    modelidx[j] = GPUs[j].index(str(gpu_av[i]))
                    break
    quick = False
    app = ''

    t0 = time.time()
    modl = [model[ii][modelidx[ii]] for ii in range(len(modelidx))]
    conf = [config[ii][modelidx[ii]] for ii in range(len(modelidx))]
    tokn = [tokenizer[ii][modelidx[ii]] for ii in range(len(modelidx))]
    devi = [device[ii][modelidx[ii]] for ii in range(len(modelidx))]
    ConfigPredict.gpus = [GPUs[ii][modelidx[ii]] for ii in range(len(modelidx))]
    if ConfigPredict.useThread:
        for D in Data:
            result = gpt_gen_thread.generating_thread(app, D['input'], modl, conf, tokn, devi, ConfigPredict, quick, num0,
                                                      removeHighFreqWordss=rmHFW, batchGenerating=batchGenerating,
                                                      tags=tags,
                                                      D_simi=D_simi, D_next=D_next, maxNext=maxNext, maxChoice=10)
            D['ouput'].extend([r + sym for r in result])
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
    modelidx_s = ','.join([str(t) for t in ConfigPredict.gpus])
    print('total inputs:{} and use time: {} s'.format(len(Data), '%0.4f' % (t1 - t0)))
    return Data
def test_myself(path_data='D:\\项目\\输入法\\数据处理\\GPT2-Chinese\\test_online\\result\\test_text4.json'):
    import random
    import json
    with open(path_data,'r',encoding='utf-8') as f:
        Data = json.load(f)
    A = []
    for ii in range(len(Data)):
        r = Data[ii]['output']
        n0 = 0
        n1 = 0
        a = []
        for i in range(len(r)):
            if '(0)' in r[i]:
                r[i] = r[i].replace('(0)','')
                tag = '0'
                n0 += 1
                if n0 < 3:
                    a.append([Data[ii]['input']] + [r[i]] + [tag])
            else:
                r[i] = r[i].replace('(1)', '')
                tag = '1'
                n1 += 1
                if n1 < 3:
                    a.append([Data[ii]['input']] + [r[i]] + [tag])
            random.shuffle(a)
        A.extend(a)
    write_excel(path_data.replace('json','xls'), A)
def test_result(path0,n0,n1):
    #path0 = 'D:\\项目\\输入法\\数据处理\\GPT2-Chinese\\test_online\\result\\test_text3.xls'
    Data = read_excel(path0)
    N0 = 0
    N1 = 0
    T0 = [0, 0, 0]
    T1 = [0, 0, 0]
    for i in range(n0,n1):
        if Data[i][4] == '0':
            N0 += 1
            T0[int(Data[i][2]) - 1] += 1
        else:
            N1 += 1
            T1[int(Data[i][2]) - 1] += 1
    print(N0, N1)
    print(T0, T1)
    print((T0[1] + T0[2]) / N0, (T1[1] + T1[2]) / N1)

def main(path_source,sym):
    print('test-begin')
    with open(path_source,'r') as f:
        Data = json.load(f)
    t0 = time.time()
    Data = test(Data,sym)
    t1 = time.time()
    print('total samples:{},used time:{} s,QPS:{}'.format(len(Data),'%0.4f'%(t1-t0),'%0.4f'%(len(Data)/(t1-t0))))
    with open(path_source.replace('.json','-new.json'),'w',encoding='utf-8') as f:
        json.dump(Data,f,ensure_ascii=False,indent=4)
    path_target = path_source.replace('.json', '-new.json').replace('.json','.xls')
    A = []
    for ii in range(len(Data)):
        a = [Data[ii]['input']]
        r = Data[ii]['ouput']
        for i in range(len(r)):
            t = r[i].split('\t')
            if len(t)==1:
                b = [t[0],'']
            else:
                b = t
            if i==0:
                a = [Data[ii]['input']]+b
            else:
                a = ['']+b
            A.append(a)
    write_excel(path_target,A)
    print('test-over')
if __name__=='__main__':
    path_source,sym=sys.argv[1:]
    main(path_source,sym)



