# coding=utf-8
import unicodedata
class config_predict(object):
    # 定义构造方法
    def __init__(self,model_config='', doPredict = [1,1,1,1]):  #__init__() 是类的初始化方法；它在类的实例化操作后 会自动调用，不需要手动调用；
        # 设置属性
        self.stopwords = [" ", "　", " ", ",", "，", ".", "。", "、", "!", "！", "?", "？", ";", "；", "~", "～", "·", "·", ".", "…", "-",
             "#_", "—", "+", "=", "'", "\"", "‘", "’", "“", "”", "*", "&", "^", "%", "$", "/", "\\", "@"]
        self.stopwords,self.map_e2z = self.addStopwords()
        self.blackwords = ['自杀','死','火葬']
        self.singlewords = ['哈','啊','哦','哦','呵','嘿','哎','哼']
        self.removed_words = ['⊙']
        self.punc_end = '.?!。？！》>'
        self.path_HighFreqWords = '../data/words_highFreq.txt'
        self.HighFreqWords = self.getHFW()
        self.min_contenlen = 8
        self.rate_gen2inp = 1.4
        self.batchGenerating = True
        self.max_nb_sents=4
        self.gpus = ['5','6','7']
        if len(model_config)==0:
            self.model_configs = ['demo_config/config_godText_large1.json', 'demo_config/config_poem.json',
                            'demo_config/config_dabaigou.json']
        else:
            if type(model_config)==list:
                self.model_configs = model_config
            else:
                self.model_configs = [model_config]
        self.predict_nums = [8, 4, 8, 5]
        self.tags = ['(文)', '(诗)', '(大白狗)', '(句联想)']
        self.doPredict = [t==1 for t in doPredict]
        self.rmHFW = [False, False, True, False]
        self.maxNext_JLX = 3
        self.path_JLX_next = 'model/nnlm/D_next.json'
        self.path_JLX_simi = 'model/nnlm/D_simi.json'
        self.prefixTrim = True
        self.useThread = True
        self.fast_pattern = True
        self.repetition_penalty = [1.2,1.5,1.2]
        self.temperature = [0.6,0.7,0.5]
        self.length = [30,64,30]
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
