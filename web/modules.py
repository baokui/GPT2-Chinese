def postprocess(S,prefix,config_postprocess,dropPerson=True,maxNbSents=True,removeEndPunc=True,removeWords = True, removeSingleWord=True,transfer = True,sentEndcontent=True,removeDupulicate=True,dropSpecial=True,removeHighFreqWords=False):
    stopwords = config_postprocess.stopwords
    map_e2z = config_postprocess.map_e2z
    blackwords = config_postprocess.blackwords
    singlewords = config_postprocess.singlewords
    removed_words = config_postprocess.removed_words
    punc_end = config_postprocess.punc_end
    HighFreqWords = config_postprocess.HighFreqWords
    min_contenlen = config_postprocess.min_contenlen
    r = config_postprocess.rate_gen2inp
    max_nb_sents=config_postprocess.max_nb_sents
    R = []
    for s0 in S:
        if removeWords:
            s0 = removewords(s0,removed_words)
        if transfer:
            s0 = prefix+Transfer(s0[len(prefix):],map_e2z)
        if sentEndcontent:
            s0 = sent_endcontent(s0,punc_end)
        if removeDupulicate:
            s0 = remove_duplicate(s0,prefix,stopwords)
        if removeSingleWord:
            s0 = remove_sents(s0,prefix,stopwords,blacksents=singlewords)
        if removeHighFreqWords:
            s0 = remove_sents(s0, prefix,stopwords, blacksents=HighFreqWords)
        if dropSpecial:
            s0 = drop_blackwords(s0,prefix,blackwords = blackwords)
        if dropPerson:
            s0 = drop_person(s0,prefix)
        if removeEndPunc:
            s0 = remove_endPunc(s0,stopwords,punc_end)
        if maxNbSents:
            s0 = sentCutting(s0,prefix,stopwords,max_nb_sents)
        if len(s0)>min_contenlen:
            if len(prefix)>10 and len(s0) - len(prefix)>5:
                R.append(s0)
                continue
            if len(prefix)>7 and len(s0) - len(prefix) > 0.8*len(prefix):
                R.append(s0)
                continue
            if len(prefix)<=7 and len(s0) - len(prefix) > r*len(prefix):
                R.append(s0)
    return R
def removewords(s0,removed_words):
    sn = s0
    for t in removed_words:
        sn = sn.replace(t,'')
    return sn
def remove_endPunc(tmptext,stopwords,punc_end):
    if len(tmptext)==0:
        return tmptext
    if tmptext[-1] in stopwords and tmptext[-1] not in punc_end:
        tmptext = tmptext[:-1]
    return tmptext
def Transfer(s0,map_e2z):
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
def drop_blackwords(s0,prefix,blackwords):
    for s in blackwords:
        if s in s0[len(prefix):]:
            return ''
    return s0
def drop_person(s0,prefix):
    if '他' not in prefix and '她' not in prefix:
        if '他' in s0 or '她' in s0:
            return ''
    return s0
def sent_endcontent(tmptext,punc_end):
    ii = 0
    for ii in range(len(tmptext)):
        if tmptext[len(tmptext) - ii - 1] in punc_end:
            break
    if ii != len(tmptext) - 1:
        tmptext = tmptext[:len(tmptext) - ii]
    return tmptext
def sent_split(s0,prefix,splitsym):
    flag = prefix[-1] not in splitsym
    L0 = []
    L = []
    i0 = 0
    i1 = 0
    while i1<len(s0):
        if s0[i1] in splitsym:
            if len(s0[i0:i1])>0 or (flag and i0==0):
                L.append(s0[i0:i1])
                L0.append(s0[i0:i1+1])
            i0 = i1+1
            i1 = i1+1
        else:
            i1 = i1+1
    if i1!=i0:
        L.append(s0[i0:i1])
        L0.append(s0[i0:i1 + 1])
    return L,L0
def remove_duplicate(s0,prefix,stopwords):
    L, L0 = sent_split(s0[len(prefix):],prefix,stopwords)
    S = []
    S0 = []
    for i in range(len(L)):
        if L[i] not in S:
            S.append(L[i])
            S0.append(L0[i])
    R = prefix+''.join(S0)
    return R
def sentCutting(s0,prefix,stopwords,max_nb_sents):
    L, L0 = sent_split(s0[len(prefix):], prefix,stopwords)
    L0 = L0[:max_nb_sents]
    L = L[:max_nb_sents]
    if len(L)==max_nb_sents:
        if len(L[-1])<4:
            L0 = L0[:-1]
    R = prefix + ''.join(L0)
    return R
def remove_sents(s0,prefix,stopwords,blacksents):
    L, L0 = sent_split(s0[len(prefix):],prefix,stopwords)
    S = []
    S0 = []
    for i in range(len(L)):
        if L[i] not in blacksents:
            S.append(L[i])
            S0.append(L0[i])
    R = prefix+''.join(S0)
    return R
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
def dropDuplicateContent(S0):
    S = []
    for s in S0:
        if s not in S:
            S.append(s)
    return S
def _is_chinese_char(char):
    """Checks whether CP is the codepoint of a CJK character."""
    # This defines a "chinese character" as anything in the CJK Unicode block:
    #   https://en.wikipedia.org/wiki/CJK_Unified_Ideographs_(Unicode_block)
    #
    # Note that the CJK Unicode block is NOT all Japanese and Korean characters,
    # despite its name. The modern Korean Hangul alphabet is a different block,
    # as is Japanese Hiragana and Katakana. Those alphabets are used to write
    # space-separated words, so they are not treated specially and handled
    # like the all of the other languages.
    cp = ord(char)
    if ((cp >= 0x4E00 and cp <= 0x9FFF) or  #
            (cp >= 0x3400 and cp <= 0x4DBF) or  #
            (cp >= 0x20000 and cp <= 0x2A6DF) or  #
            (cp >= 0x2A700 and cp <= 0x2B73F) or  #
            (cp >= 0x2B740 and cp <= 0x2B81F) or  #
            (cp >= 0x2B820 and cp <= 0x2CEAF) or
            (cp >= 0xF900 and cp <= 0xFAFF) or  #
            (cp >= 0x2F800 and cp <= 0x2FA1F)):  #
        return True
    return False
def sentTriming(s0='@Charon 你打的咋样'):
    s = s0
    if s[0]=='@':
        idx = s.find(' ')
        if idx!=-1:
            s = s[idx+1:]
    tmp = list(s[:-1])
    for t in tmp:
        if not _is_chinese_char(t):
            s = s.replace(t,'')
    return s
def findMaxMatch(inputStr,D_simi,D_next):
    if inputStr in D_next:
        return inputStr
    if inputStr in D_simi:
        return inputStr
    if len(inputStr)<3:
        return ''
    L = [d for d in D_next]+[d for d in D_simi]
    i = len(inputStr)-3
    prefix = ''
    while i>=0:
        s = inputStr[i:]
        if s in L:
            prefix = s
        else:
            break
        i -= 1
    return prefix
