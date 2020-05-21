# coding=utf-8
import unicodedata
class Config(object):
    # 定义构造方法
    def __init__(self):  #__init__() 是类的初始化方法；它在类的实例化操作后 会自动调用，不需要手动调用；
        # 设置属性
        self.stopwords = [" ", "　", " ", ",", "，", ".", "。", "、", "!", "！", "?", "？", ";", "；", "~", "～", "·", "·", ".", "…", "-",
             "#_", "—", "+", "=", "'", "\"", "‘", "’", "“", "”", "*", "&", "^", "%", "$", "/", "\\", "@"]
        self.stopwords,self.map_e2z = self.addStopwords()
        self.blackwords = ['自杀','死','葬','我是你爸','我是你妈','已故','无生路',
                           '有病','贱','逼', '操','艹','禽兽','混蛋','滚蛋','sb','脱',
                           '扑街','笨蛋','废物','蠢蛋','蠢货','傻','2B','智障',
                           '脑残','白痴','三八','无赖','低能','弱智','二痴','蛋白质',
                           '王八','贱人','小兔崽子','胡说八道','蛮不讲理','神经兮兮',
                           '不得好死','臭不要脸','死皮赖脸','令人发指', '狼心狗肺',
                           '狼狈为奸', '水性杨花','薄情寡义','负心薄幸','朝三暮四',
                           '卑鄙下流','不知廉耻','勾心斗角','猪狗不如','缺',
                           '肏','我草','我干','我去','我操','你妈','尼玛','杂种',
                           '卧槽','屌','鸡巴','干你娘','操你','老屁眼','骚货','日你','婊子',
                           '你他妈','草你','麻批','欠操','操他','操她','丢你老母',
                           '吸毒','恋童','共产党','毒']
        self.blackwords_inputs = ['汶川','吸毒','恋童','共产党','毒']
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
