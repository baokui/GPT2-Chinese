import unicodedata
stopwords = [" ", "　", " ", ",", "，", ".", "。", "、", "!", "！", "?", "？", ";", "；", "~", "～", "·", "·", ".", "…", "-",
             "#_", "—", "+", "=", "'", "\"", "‘", "’", "“", "”", "*", "&", "^", "%", "$", "/", "\\", "@"]
punc_zh = "！？｡＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟‧﹏.…"
punc_en = unicodedata.normalize('NFKC', punc_zh[:-1])+unicodedata.normalize('NFKC', punc_zh[-1])[-1]
punc_zh = punc_zh+'。'
punc_en = punc_en+'｡'
map_e2z = {punc_en[i]:punc_zh[i] for i in range(len(punc_en))}
stopwords = stopwords+list(punc_zh)+list(punc_en)
stopwords = list(set(stopwords))
blackwords = ['他','她','自杀','死']
remove_words = ['⊙']
removedPunc = [',.，']
def remove_stopwords(s0,stopwords0=stopwords):
    sn = s0
    for t in stopwords0:
        sn = sn.replace(t,'')
    return sn
def postprocess(S,prefix,removeEndPunc=True,removeWords = True, transfer = True,sentEndcontent=True,removeDupulicate=True,removeSpecial=True,removeHighFreqWords=False,HighFreqWords=[],min_contenlen=8,r=1.5):
    R = []
    for s0 in S:
        if removeWords:
            s0 = remove_stopwords(s0,remove_words)
        if transfer:
            s0 = prefix+Transfer(s0[len(prefix):])
        if sentEndcontent:
            s0 = sent_endcontent(s0)
        if removeDupulicate:
            s0 = remove_duplicate(s0,removeHighFreqWords,HighFreqWords)
        if removeSpecial:
            s0 = remove_special(s0)
        if removeEndPunc:
            s0 = remove_endPunc(s0)
        if len(s0)>min_contenlen and len(s0)-len(prefix)> r*len(prefix):
            R.append(s0)
    return R
def remove_endPunc(s0):
    if len(s0)>0:
        if s0[-1] in removedPunc:
            s0 = s0[:-1]
    return s0
def Transfer(s0):
    s0 = strQ2B(s0)
    for t in map_e2z:
        if t in s0:
            s0 = s0.replace(t,map_e2z[t])
    return s0
def strQ2B(ustring):
    """全角转半角"""
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 12288:  # 全角空格直接转换
            inside_code = 32
        elif (inside_code >= 65281 and inside_code <= 65374):  # 全角字符（除空格）根据关系转化
            inside_code -= 65248
        rstring += chr(inside_code)
    return rstring
def strB2Q(ustring):
    """半角转全角"""
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 32:  # 半角空格直接转化
            inside_code = 12288
        elif inside_code >= 32 and inside_code <= 126:  # 半角字符（除空格）根据关系转化
            inside_code += 65248
        rstring += chr(inside_code)
    return rstring
def remove_special(s0):
    spe = blackwords
    for s in spe:
        if s in s0:
            return ''
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
def remove_duplicate(s0,removeHighFreqWords=False,HighFreqWords=[]):
    stopwords = [" ", "　", " ", ",", "，", ".", "。", "、", "!", "！", "?", "？", ";", "；", "~", "～", "·", "·", ".", "…",
                 "-", "#_", "—", "+", "=", "'", "\"", "‘", "’", "“", "”", "*", "&", "^", "%", "$", "/", "\\", "@"]
    L0 = []
    L = []
    i0 = 0
    for i0 in range(len(s0)):
        if s0[i0] in stopwords:
            break
    L0.append(s0[:i0+1])
    L.append(s0[:i0])
    i0 = i0+1
    i1 = i0
    flag_hfw = True
    while i1<len(s0):
        if s0[i1] in stopwords:
            if i1>i0:
                a = s0[i0:i1]
                if a not in L:
                    if removeHighFreqWords:
                        if a in HighFreqWords:
                            if flag_hfw:
                                L0.append(a+s0[i1])
                                L.append(a)
                                flag_hfw = False
                        else:
                            L0.append(a + s0[i1])
                            L.append(a)
                    else:
                        L0.append(a + s0[i1])
                        L.append(a)
            i0 = i1+1
            i1 = i1+1
        elif i1==len(s0)-1:
            a = s0[i0:]
            if a not in L:
                if removeHighFreqWords:
                    if a in HighFreqWords:
                        if flag_hfw:
                            L0.append(a)
                            L.append(a)
                            flag_hfw = False
                    else:
                        L0.append(a)
                        L.append(a)
                else:
                    L0.append(a)
                    L.append(a)
            break
        else:
            i1 = i1+1
    R = ''.join(L0)
    if len(R)>0:
        if R[-1] in stopwords:
            R = R[:-1]
    return R

def remove_highFreqWords(s0,path_highFreqWords):
    stopwords = [" ", "　", " ", ",", "，", ".", "。", "、", "!", "！", "?", "？", ";", "；", "~", "～", "·", "·", ".", "…",
                 "-", "#_", "—", "+", "=", "'", "\"", "‘", "’", "“", "”", "*", "&", "^", "%", "$", "/", "\\", "@"]
    L0 = []
    L = []
    i0 = 0
    i1 = 0
    while i1 < len(s0):
        if s0[i1] in stopwords:
            if i1 > i0:
                a = s0[i0:i1]
                if a not in L:
                    L0.append(a + s0[i1])
                    L.append(a)
            i0 = i1 + 1
            i1 = i1 + 1
        else:
            i1 = i1 + 1
    R = ''.join(L0)
def poemFilter(poem):
    flag = True
    syms = '。？；'
    sents = []
    i0 = 0
    i1 = 0
    while i1<len(poem):
        if poem[i1] in syms:
            sents.append(poem[i0:i1])
            i0 = i1+1
            i1 = i1+1
        else:
            i1 = i1+1
    if i1>i0:
        sents.append(poem[i0:i1])
    if len(sents)==0:
        return False
    n = [len(s) for s in sents]
    if max(n)!=min(n):
        flag = False
    for s in sents:
        ws = s.split('，')
        if len(ws)!=2:
            flag = False
            break
        if len(ws[0])!=len(ws[1]):
            flag = False
            break
    if not flag:
        flag = False
    return flag
def poemFilter1(poem):
    syms = '。？；'
    sents = []
    i0 = 0
    i1 = 0
    while i1<len(poem):
        if poem[i1] in syms:
            sents.append(poem[i0:i1+1])
            i0 = i1+1
            i1 = i1+1
        else:
            i1 = i1+1
    R = []
    for i in range(len(sents)):
        if len(sents[i])==len(sents[0]):
            R.append(sents[i])
    if len(R)>1:
        return ''.join(R)
    else:
        return ''
