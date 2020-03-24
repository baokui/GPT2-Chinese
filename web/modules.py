import unicodedata
stopwords = [" ", "　", " ", ",", "，", ".", "。", "、", "!", "！", "?", "？", ";", "；", "~", "～", "·", "·", ".", "…", "-",
             "#_", "—", "+", "=", "'", "\"", "‘", "’", "“", "”", "*", "&", "^", "%", "$", "/", "\\", "@"]
punc_zh = "！？｡＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟‧﹏.…"
punc_en = unicodedata.normalize('NFKC', punc_zh[:-1])+unicodedata.normalize('NFKC', punc_zh[-1])[-1]
map_e2z = {punc_en[i]:punc_zh[i] for i in range(len(punc_en))}
stopwords = stopwords+list(punc_zh)+list(punc_en)
stopwords = list(set(stopwords))
def remove_stopwords(s0):
    sn = s0
    for t in stopwords:
        sn = sn.replace(t,'')
    return sn
def postprocess(S,prefix,transfer = True,sentEndcontent=True,removeDupulicate=True,removeSpecial=True,min_contenlen=8,r=1.5):
    R = []
    for s0 in S:
        if transfer:
            s0 = Transfer(s0)
        if sentEndcontent:
            s0 = sent_endcontent(s0)
        if removeDupulicate:
            s0 = remove_duplicate(s0)
        if removeSpecial:
            s0 = remove_special(s0)
        if len(s0)>min_contenlen and len(s0)-len(prefix)> r*len(prefix):
            R.append(s0)
    return R
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
    spe = '他她'
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