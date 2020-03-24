def remove_stopwords(s0):
    stopwords = [" ","　"," ",",","，",".","。","、","!","！","?","？",";","；","~","～","·","·",".","…","-","#_","—","+","=","'","\"","‘","’","“","”","*","&","^","%","$","/","\\","@"]
    sn = s0
    for t in stopwords:
        sn = sn.replace(t,'')
    return sn
def postprocess(s0,sentEndcontent=True,removeDupulicate=True):
    if sentEndcontent:
        s0 = sent_endcontent(s0)
    if removeDupulicate:
        s0 = remove_duplicate(s0)
    return s0
def sent_endcontent(tmptext):
    punc_end = '.?!。？！'
    ii =  0
    for ii in range(len(tmptext)):
        if tmptext[len(tmptext) - ii - 1] in punc_end:
            break
    if ii != len(tmptext) - 1:
        tmptext = tmptext[:len(tmptext) - ii]
    return tmptext
def remove_duplicate(s0="眼疾手快，相信自己哈，我也是，哈哈哈，我也是，我也是，嗯，不知道，我妈不让我出去，哈哈哈，我也是，哈哈哈，嗯，我也是，哈""眼疾手快，相信自己哈，我也是，哈哈哈，我也是，我也是，嗯，不知道，我妈不让我出去，哈哈哈，我也是，哈哈哈，嗯，我也是，哈"):
    stopwords = [" ", "　", " ", ",", "，", ".", "。", "、", "!", "！", "?", "？", ";", "；", "~", "～", "·", "·", ".", "…",
                 "-", "#_", "—", "+", "=", "'", "\"", "‘", "’", "“", "”", "*", "&", "^", "%", "$", "/", "\\", "@"]
    L0 = []
    L = []
    i0 = 0
    i1 = 0
    while i1<len(s0):
        if s0[i1] in stopwords:
            if i1>i0:
                a = s0[i0:i1]
                if a not in L:
                    L0.append(a+s0[i1])
                    L.append(a)
            i0 = i1+1
            i1 = i1+1
        else:
            i1 = i1+1
    R = ''.join(L0)
    if len(R)>0:
        if R[-1] in stopwords:
            R = R[:-1]
    return R