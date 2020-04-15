import json
import os
def dataPro01(path_source,path_target):
    rootpath = '../data/GodText/01/'
    path_source = os.path.join(rootpath,'godText_all1.json')
    with open(path_source,'r') as f:
        S0 = json.load(f)
    S1 = []#没有新年祝福
    S2 = []#只有新年祝福
    s = ['新年','新春','春节','元旦','鼠年','牛年','虎年','兔年','龙年','蛇年','马年','羊年','猴年','鸡年','狗年','猪年']
    for i in range(len(S0)):
        flag = True
        for t in s:
            if t in S0[i]:
                S2.append(S0[i])
                flag = False
                break
        if flag:
            S1.append(S0[i])
        if i%10000==0:
            print(i,len(S0),len(S1),len(S2))
    print(len(S0),len(S1),len(S2))
    with open(os.path.join(rootpath,'S0.json'),'w') as f:
        json.dump(S0,f,ensure_ascii=False,indent=4)
    with open(os.path.join(rootpath,'S1.json'),'w') as f:
        json.dump(S1,f,ensure_ascii=False,indent=4)
    with open(os.path.join(rootpath,'S2.json'),'w') as f:
        json.dump(S2,f,ensure_ascii=False,indent=4)
def dataPro02():
    import xlrd
    rootpath = '../data/GodText/02/'
    path_source1 = os.path.join(rootpath,'神配文-2期-清洗完成.xlsx')
    path_source2 = os.path.join(rootpath,'未清洗')
    workbook = xlrd.open_workbook(path_source1)  # 打开excel文件
    sheets = workbook.sheets()
    R = []
    for i in range(1,len(sheets)):
        table = workbook.sheet_by_name(sheets[i].name)  # 将文件内容表格化
        rows_num = table.nrows  # 获取行
        cols_num = table.ncols  # 获取列
        res = []  # 定义一个数组
        for rows in range(rows_num):
            r = []
            for cols in range(cols_num):
                r.append(table.cell(rows, cols).value)  # 获取excel中单元格的内容
            res.append(r)
        R.extend([res[j][0] for j in range(1,len(res))])
    S0 = R
    S1 = []  # 没有新年祝福
    S2 = []  # 只有新年祝福
    s = ['新年', '新春', '春节', '元旦', '鼠年', '牛年', '虎年', '兔年', '龙年', '蛇年', '马年', '羊年', '猴年', '鸡年', '狗年', '猪年']
    for i in range(len(S0)):
        flag = True
        for t in s:
            if t in S0[i]:
                S2.append(S0[i])
                flag = False
                break
        if flag:
            S1.append(S0[i])
        if i % 10000 == 0:
            print(i, len(S0), len(S1), len(S2))
    print(len(S0), len(S1), len(S2))
    with open(os.path.join(rootpath, 'S0_washed.json'), 'w') as f:
        json.dump(S0, f, ensure_ascii=False, indent=4)
    with open(os.path.join(rootpath, 'S1_washed.json'), 'w') as f:
        json.dump(S1, f, ensure_ascii=False, indent=4)
    with open(os.path.join(rootpath, 'S2_washed.json'), 'w') as f:
        json.dump(S2, f, ensure_ascii=False, indent=4)

    S0 = []
    files = os.listdir(path_source2)
    for file in files:
        f = open(os.path.join(path_source2,file),'r')
        s = f.read().strip().split('\n')
        S0.extend([t.split('\t')[0] for t in s if len(t.split('\t'))==4])
        print(len(S0))
    S1 = []  # 没有新年祝福
    S2 = []  # 只有新年祝福
    s = ['新年', '新春', '春节', '元旦', '鼠年', '牛年', '虎年', '兔年', '龙年', '蛇年', '马年', '羊年', '猴年', '鸡年', '狗年', '猪年']
    for i in range(len(S0)):
        flag = True
        for t in s:
            if t in S0[i]:
                S2.append(S0[i])
                flag = False
                break
        if flag:
            S1.append(S0[i])
        if i % 10000 == 0:
            print(i, len(S0), len(S1), len(S2))
    print(len(S0), len(S1), len(S2))
    with open(os.path.join(rootpath, 'S0_nowashed.json'), 'w') as f:
        json.dump(S0, f, ensure_ascii=False, indent=4)
    with open(os.path.join(rootpath, 'S1_nowashed.json'), 'w') as f:
        json.dump(S1, f, ensure_ascii=False, indent=4)
    with open(os.path.join(rootpath, 'S2_nowashed.json'), 'w') as f:
        json.dump(S2, f, ensure_ascii=False, indent=4)
def mergeall():
    from modules import Config,Transfer,is_chinese_char,getVocab
    config = Config()
    min_len = 10
    useLower = True
    useE2Z = True
    path_target = '../data/GodText/merge/godText_noXinNian.json'
    path_vocab = '../data/GodText/merge/vocab.txt'
    paths = ['../data/GodText/01/S1.json']
    paths.append('../data/GodText/02/S1_washed.json')
    paths.append('../data/GodText/02/S1_nowashed.json')
    S0 = []
    for path in paths:
        with open(path,'r') as f:
            S0.extend(json.load(f))
    S = []
    for i in range(len(S0)):
        s = S0[i]
        if len(s)<min_len:
            continue
        if useLower:
            s = s.lower()
        if useE2Z:
            s = Transfer(s,config.map_e2z)
        while not is_chinese_char(s[0]):
            s = s[1:]
            if len(s)<=1:
                break
        if len(s)<min_len:
            continue
        S.append(s)
        if i%10000==0:
            print(i,len(S0),len(S))
    random.shuffle(S)
    with open(path_target,'w') as f:
        json.dump(S,f,ensure_ascii=False,indent=4)
    L=getVocab(S,0)
    V0 = ['[PAD]','[UNK]','[CLS]','[SEP]','[MASK]','<S>','<T>']+['unused'+str(i) for i in range(10)]

    V = V0 + [L[i][0] for i in range(5000)]
    with open(path_vocab,'w') as f:
        f.write('\n'.join(V))