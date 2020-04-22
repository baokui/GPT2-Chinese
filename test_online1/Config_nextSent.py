# coding=utf-8
from Config import Config
class config_predict(Config):
    # 定义构造方法
    def __init__(self):  #__init__() 是类的初始化方法；它在类的实例化操作后 会自动调用，不需要手动调用；
        super().__init__()
        self.min_contenlen = 8
        self.rate_gen2inp = 1.4
        self.predict_nums = 5
        self.tags = '(句联想)'
        self.rmHFW = False
        self.maxNext_JLX = 3
        self.path_JLX_next = '../bin/model/nnlm/D_next.json'
        self.path_JLX_simi = '../bin/model/nnlm/D_simi.json'
