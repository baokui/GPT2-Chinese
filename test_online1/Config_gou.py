# coding=utf-8
import unicodedata
from Config import Config
class config_predict(Config):
    # 定义构造方法
    def __init__(self):  #__init__() 是类的初始化方法；它在类的实例化操作后 会自动调用，不需要手动调用；
        self.gpus = ',,'
        self.model_configs = '../bin/config/config_dabaigou.json'
        self.predict_nums = 8
        self.tags = '(大白狗)'
        self.rmHFW = True
        self.prefixTrim = True
        self.fast_pattern = True
        self.repetition_penalty = 1.2
        self.temperature = 0.5
        self.length = 30
        self.resort = True
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
