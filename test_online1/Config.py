# coding=utf-8
import unicodedata
class Config(object):
    # 定义构造方法
    def __init__(self):  #__init__() 是类的初始化方法；它在类的实例化操作后 会自动调用，不需要手动调用；
        # 设置属性
        self.stopwords = [" ", "　", " ", ",", "，", ".", "。", "、", "!", "！", "?", "？", ";", "；", "~", "～", "·", "·", ".", "…", "-",
             "#_", "—", "+", "=", "'", "\"", "‘", "’", "“", "”", "*", "&", "^", "%", "$", "/", "\\", "@"]
        self.stopwords,self.map_e2z = self.addStopwords()
        self.blackwords = ['自杀','死','火葬']
        self.specialwords_pre = ['祝福', '祝愿', '预祝']
        self.specialwords_gen = ['生日','新年','新春','春节','节日','元旦']
        self.singlewords = ['哈','啊','哦','哦','呵','嘿','哎','哼']
        self.removed_words = ['⊙']
        self.punc_end = '.?!。？！》>'
        self.path_HighFreqWords = '../bin/data/words_highFreq.txt'
        self.HighFreqWords = self.getHFW()
        self.min_contenlen = 8
        self.rate_gen2inp = 1.4
        self.batchGenerating = True
        self.max_nb_sents=4
        self.prefixTrim = True
        self.useThread = False
        self.fast_pattern = True
    def addStopwords(self):
        punc_zh = "！？｡＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟‧﹏.…"
        punc_en = unicodedata.normalize('NFKC', punc_zh[:-1]) + unicodedata.normalize('NFKC', punc_zh[-1])[-1]
        punc_zh = punc_zh + '。'
        punc_en = punc_en + '｡'
        map_e2z = {punc_en[i]: punc_zh[i] for i in range(len(punc_en))}
        stopwords = self.stopwords + list(punc_zh) + list(punc_en)
        stopwords = list(set(stopwords))
        return stopwords,map_e2z
    def getHFW(self):
        with open(self.path_HighFreqWords,'r') as f:
            s = f.read().strip().split('\n')
        return s
