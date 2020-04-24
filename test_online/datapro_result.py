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
def test_result(path0,n0,n1):
    #path0 = 'D:\\项目\\输入法\\数据处理\\GPT2-Chinese\\test_online\\result\\test_text3.xls'
    Data = read_excel(path0)
    N0 = 0
    N1 = 0
    N2 = 0
    T0 = [0, 0, 0]
    T1 = [0, 0, 0]
    T2 = [0,0,0]
    for i in range(n0,n1):
        if Data[i][4] == '0':
            N0 += 1
            T0[int(Data[i][2]) - 1] += 1
        elif Data[i][4]=='1':
            N1 += 1
            T1[int(Data[i][2]) - 1] += 1
        else:
            N2 += 1
            T2[int(Data[i][2]) - 1] += 1
    print(N0, N1,N2)
    print(T0, T1,T2)
    print((T0[1] + T0[2]) / N0, (T1[1] + T1[2]) / N1,(T2[1] + T2[2]) / N2)
def getdata():
    paths = ['D:\项目\输入法\神配文数据\生成评测\固定评测集200条.xlsx']
    for p in paths:
        data = read_excel(p)
    S = []
    predix = ''
    for i in range(1,len(data)):
        if data[i][0]!='':
            predix = data[i][0]
        if '(文)' in data[i][3] and data[i][8]!='':
            S.append([predix,data[i][3],data[i][8]])