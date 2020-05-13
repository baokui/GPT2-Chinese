import requests
import time
import sys
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
def main(url,path_data,tails=''):
    t0 = time.time()
    #url = url0+port+"/api/gen"
    #path_data = 'data/test_text.txt'
    with open(path_data,'r') as f:
        s = f.read().strip().split('\n')
    R = []
    for str in s:
        data = {"input":str+tails}
        res = requests.post(url=url,json=data)
        #if res.json()['message']!='success':
            #print(res.json())
        R.append(res.json())
    t1 = time.time()
    #print('number of samles:{},total time:{}s, QPS:{}'.format(len(s),'%0.4f'%(t1-t0),'%0.4f'%(len(s)/(t1-t0))))
    return R
def demo0():
    path_data='data/test_headlove.txt'
    url = 'http://10.141.104.42:5000/api/gen'
    tails = '#hdlv'
    R = main(url,path_data,tails)
    maxnb = 0
    D = []
    res = []
    for r in R:
        words = r['input']
        T = r['result']
        T = [t for t in T if '(诗)' in t]
        T = [t.replace('(诗)','') for t in t]
        if maxnb<len(T):
            maxnb = len(T)
        res.append([words]+T)
    for i in range(len(res)):
        if len(res[i])<maxnb+1:
            res[i].extend(['']*(maxnb+1-len(res[i])))
    write_excel('data/test_headlove.xls', res)



if __name__=='__main__':
    port = sys.argv[1]
    url0 = sys.argv[2]
    main(url0,port)