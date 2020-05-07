# -*- encoding: utf-8 -*-
import json
import gpt_gen
import gpt_gen_thread
import sys
from Config_compare import *
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

def predict(Data):
    quick = False
    R = []
    app = ''
    for data in Data:
        result = gpt_gen_thread.generating_thread(app, data, model, config, tokenizer, device, ConfigPredict,quick, num0,
                                                   removeHighFreqWordss=rmHFW, batchGenerating=batchGenerating,tags=tags,
                                                  D_simi=D_simi,D_next=D_next,maxNext=maxNext,maxChoice=10)

        R.append({'input':data,'output':result})
    return R
def main(path_source,path_target):
    with open(path_source,'r',encoding='utf-8') as f:
        s = f.read().strip().split('\n')
    R = predict(s)
    with open(path_target,'w',encoding='utf-8') as f:
        json.dump(R,f,ensure_ascii=False,indent=4)
# start flask app
if __name__ == '__main__':
    path_source,path_target = sys.argv[2:4]
    nb_models = sys.argv[1]
    ConfigPredict = []
    ConfigPredict.append(config_predict0())
    ConfigPredict.append(config_predict1())
    if nb_models == '3':
        ConfigPredict.append(config_predict2())
    batchGenerating = ConfigPredict[0].batchGenerating
    path_configs = [c.model_configs for c in ConfigPredict]
    num0 = [c.predict_nums for c in ConfigPredict]
    tags = [c.tags for c in ConfigPredict]
    rmHFW = [c.rmHFW for c in ConfigPredict]
    '''
    maxNext = ConfigPredict.maxNext_JLX
    path_next = ConfigPredict.path_JLX_next
    path_simi = ConfigPredict.path_JLX_simi
    D_simi = json.load(open(path_simi,'r',encoding='utf-8'))
    D_next = json.load(open(path_next,'r',encoding='utf-8'))
    D_simi = {k:json.loads(D_simi[k]) for k in D_simi}
    D_next = {k:json.loads(D_next[k]) for k in D_next}
    '''
    D_simi, D_next, maxNext = [], [], []
    model, tokenizer, config, device = [], [], [], []
    for ii in range(len(path_configs)):
        m0, t0, c0, d0 = gpt_gen.getModel(path_config=path_configs[ii], gpu=ConfigPredict[ii].gpus)
        c0['repetition_penalty'] = ConfigPredict[ii].repetition_penalty
        c0['temperature'] = ConfigPredict[ii].temperature
        c0['length'] = ConfigPredict[ii].length
        model.append(m0)
        tokenizer.append(t0)
        config.append(c0)
        device.append(d0)
    main(path_source,path_target)
