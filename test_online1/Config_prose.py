# coding=utf-8
from Config import Config
class config_predict(Config):
    # 定义构造方法
    def __init__(self, model_config='', gpus=''):  # __init__() 是类的初始化方法；它在类的实例化操作后 会自动调用，不需要手动调用；
        super().__init__()
        if gpus:
            self.gpus = gpus
        else:
            self.gpus = '0'
        if model_config:
            self.model_configs = model_config
        else:
            #self.model_configs = '../bin/config/config_godText_small_finetune.json'
            self.model_configs = '../bin/config/config_godText_large1.json'
        self.predict_nums = 8
        self.tags = '(文)'
        self.rmHFW = False
        self.repetition_penalty = 1.2
        self.temperature = 0.6
        self.length = 30
        self.resort = True

