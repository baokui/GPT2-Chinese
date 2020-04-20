import sys
import json
from app import *
import numpy as np
import time
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
def test(Data):
    def test2():
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
        if "quick" in r:
            print("quick pattern")
            if r["quick"] == "True":
                quick = True
        app = ''
        try:
            t0 = time.time()
            modl = [model[ii][modelidx[ii]] for ii in range(len(modelidx))]
            conf = [config[ii][modelidx[ii]] for ii in range(len(modelidx))]
            tokn = [tokenizer[ii][modelidx[ii]] for ii in range(len(modelidx))]
            devi = [device[ii][modelidx[ii]] for ii in range(len(modelidx))]
            ConfigPredict.gpus = [GPUs[ii][modelidx[ii]] for ii in range(len(modelidx))]
            if ConfigPredict.useThread:
                R = []
                for D in Data:
                    d = D['input']
                    result = gpt_gen_thread.generating_thread(app, data, modl, conf, tokn, devi, ConfigPredict, quick, num0,
                                                          removeHighFreqWordss=rmHFW, batchGenerating=batchGenerating,
                                                          tags=tags,
                                                          D_simi=D_simi, D_next=D_next, maxNext=maxNext, maxChoice=10)
                    D['output'].append([r+'(new)' for r in result])
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
            print('gpus {}-th (opt is {}) string and use time: {} s'.format(modelidx_s, gpu_opt, '%0.4f' % (t1 - t0)))
        except Exception as e:
            pass
def main(path_source):
    with open(path_source,'r') as f:
        Data = json.load(f)
    test(Data)
    with open(path_source.replace('.json','-new.json'),'w',encoding='utf-8') as f:
        json.dump(Data,f,ensure_ascii=False,indent=4)
if __name__=='__main__':
    path_source=sys.argv[1]
    main(path_source)