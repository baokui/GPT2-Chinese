import numpy as np
def postprocess(S,prefix,config_postprocess,specialWordFilter=True,dropPerson=True,maxNbSents=True,removeEndPunc=True,removeWords = True, removeSingleWord=True,transfer = True,sentEndcontent=True,removeDupulicate=True,dropSpecial=True,removeHighFreqWords=False,removeIncompletePunc=True):
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
    specialwords_pre = config_postprocess.specialwords_pre
    specialwords_gen = config_postprocess.specialwords_gen
    R = []
    for s0 in S:
        if specialWordFilter:
            if not hasSpectialWords(s0,prefix,specialwords_pre,specialwords_gen):
                continue
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
        if maxNbSents:
            s0 = sentCutting(s0,prefix,stopwords,max_nb_sents,punc_end)
        if removeEndPunc:
            s0 = remove_endPunc(s0,stopwords,punc_end)
        if removeIncompletePunc:
            if not hasCompletePunc(s0[len(prefix):]):
                continue
        if len(s0)>min_contenlen:
            if len(set(s0[len(prefix):]))==1:
                continue
            if len(prefix)>10 and len(s0) - len(prefix)>5:
                R.append(s0)
                continue
            if len(prefix)>7 and len(s0) - len(prefix) > 0.8*len(prefix):
                R.append(s0)
                continue
            if len(prefix)<=7 and len(s0) - len(prefix) > r*len(prefix):
                R.append(s0)
    return R
def hasSpectialWords(s0,prefix,specialwords_pre,specialwords_gen):
    for t in specialwords_pre:
        if t in prefix:
            return True#可以包含特殊词汇
    s1 = s0[len(prefix):]
    for t in specialwords_gen:
        if t in s1:
            return False#句首没有特殊词汇，那么生成文本不能包含特殊词汇
    return True
def removewords(s0,removed_words):
    sn = s0
    for t in removed_words:
        sn = sn.replace(t,'')
    return sn
def hasCompletePunc(s):
    L = ['(', '<', '{', '[', '‘', '“', '《', '［', '（', '【']
    R = [')', '>', '}', ']', '’', '”', '》', '］', '）', '】']
    D = {k:0 for k in L}
    Flag = True
    for i in range(len(s)):
        if s[i] in L:
            D[s[i]] += 1
            continue
        if s[i] in R:
            idx = R.index(s[i])
            if D[L[idx]]==0:
                Flag = False
                break
            D[L[idx]]-=1
    for d in D:
        if D[d]!=0:
            Flag = False
    if Flag:
        n0 = s.count('\'')
        if n0%2==0:
            n1 = s.count('"')
            if n1%2!=0:
                Flag=False
        else:
            Flag = False
    return Flag
def remove_endPunc(tmptext,stopwords,punc_end):
    if len(tmptext)==0:
        return tmptext
    if tmptext[-1] in stopwords and tmptext[-1] not in punc_end:
        tmptext = tmptext[:-1]
        tmptext = tmptext+'。'
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
def sentCutting(s0,prefix,stopwords,max_nb_sents,punc_end):
    A, A0 = sent_split(s0[len(prefix):], prefix,stopwords)
    L = [A[i] for i in range(len(A)) if len(A[i])>1]
    L0 = [A0[i] for i in range(len(A)) if len(A[i])>1]
    L0 = L0[:max_nb_sents]
    L = L[:max_nb_sents]
    if len(L)==max_nb_sents:
        if len(L[-1])<4:
            L0 = L0[:-1]
    if len(s0)>5*len(prefix):
        if len(L0)>0 and len(s0)-len(L0[-1])>4*len(prefix) and L0[-1][-1] not in punc_end:
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
    syms = '。？；！，'
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
    if len(sents)<2:
        return ''
    R = []
    R.append(sents[0])
    R.append(sents[1])
    for i in range(1,int(len(sents)/2)):
        if len(sents[2*i])==len(sents[0]) and len(sents[2*i+1])==len(sents[1]):
            R.append(sents[2*i])
            R.append(sents[2*i+1])
    if len(R)>2 and len(R[0])>3:
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
def findMaxMatch(inputStr,D_simi,D_next,config_predict):
    punc = ''
    i = len(inputStr)-1
    while i>0:
        if inputStr[i] in config_predict.stopwords:
            punc += inputStr[i]
        else:
            break
        i -= 1
    inputStr = inputStr[:i+1]
    if inputStr in D_next:
        return inputStr,punc
    if inputStr in D_simi:
        return inputStr,punc
    if len(inputStr)<3:
        return '',punc
    L = [d for d in D_next]+[d for d in D_simi]
    i = len(inputStr)-3
    prefix = ''
    while i>=0:
        s = inputStr[i:]
        if s in L:
            prefix = s
        i -= 1
    return prefix,punc
def resort(prefix,S,config,useNumSents=True,useSentLen=True,useNumLessChar=True,useMaxMinLen=False,useStdSentLen=True):
    Score = []
    stopwords = config.stopwords
    W = [1000,100,10,1]
    len_prefix = len(prefix)
    for sent in S:
        score = []
        sents,sents0 = sent_split(sent,prefix,stopwords)
        if useNumSents:
            nb = len(sents)
            t = 0
            if nb==3:
                t = 1
            if nb==4:
                t = 0.5
            score.append(t)
        if useSentLen:
            t = 0
            len_sent = len(sent)
            if len(prefix)<10:
                if len_sent > len_prefix*2.5 and len_sent < len_prefix*3.5:
                    t = 1
                elif len_sent < len_prefix*1.5 or len_sent > len_prefix*5:
                    t = -1
            else:
                if len_sent > len_prefix*1.5 and len_sent < len_prefix*2.5:
                    t = 1
                elif len_sent < len_prefix*0.5 or len_sent > len_prefix*3:
                    t = -1
            score.append(t)
        if useNumLessChar:
            n = len([t for t in sents if len(t)<=3])
            t = 0
            if n>2:
                t = -1
            if n==2:
                t = -0.7
            if n==1:
                t = -0.5
            score.append(t)
        if useMaxMinLen:
            p = [len(t) for t in sents]
            a = (max(p)-min(p))/max(p)
            score.append(-a)
        if useStdSentLen:
            t = -3
            a = [len(k) for k in sents]
            if len(a)>2:
                t = -np.std(a,ddof=1)
            if len(a)==2:
                t = -2
            score.append(t)
        Score.append(score)
    Score = np.array(Score)
    Max = np.max(Score,axis=0)
    Min = np.min(Score,axis=0)
    eps = 1e-5
    Score = (Score-Min)/(Max-Min+eps)
    Score = np.sum(Score,axis=-1)
    R = [(S[i],Score[i]) for i in range(len(S))]
    R = sorted(R,key=lambda x:-x[-1])
    R = [r[0] for r in R]
    return R
def demo_resort():
    path_data = 'data/test_text.txt'
    path_source = 'result/test_text.json'
    path_target = 'result/test_text-resort.json'
    from Config import config_predict
    import json
    config = config_predict()
    with open(path_data,'r') as f:
        Data = f.read().strip().split('\n')
    with open(path_source,'r') as f:
        S = json.load(f)
    D = []
    for i in range(len(Data)):
        prefix = Data[i]
        outputs = S[i]['result']
        s1 = [s[:-3] for s in outputs if '(文)' in s]
        s2 = [s[:-5] for s in outputs if '(大白狗)' in s]
        if len(s1)==0:
            r1 = []
        else:
            r1 = resort(prefix,s1,config)
        if len(s2)==0:
            r2 = []
        else:
            r2 = resort(prefix,s2,config)
        R = [r+'(文)' for r in r1]
        R += [r+'(大白狗)' for r in r2]
        d = {'input':prefix,'outputs':R}
        D.append(d)
    with open(path_target,'w') as f:
        json.dump(D,f,ensure_ascii=False,indent=4)
