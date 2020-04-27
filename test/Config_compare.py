# coding=utf-8
from Config import Config
class config_predict0(Config):
    # 定义构造方法
    def __init__(self, model_config='', gpus=''):  # __init__() 是类的初始化方法；它在类的实例化操作后 会自动调用，不需要手动调用；
        super().__init__()
        if gpus:
            self.gpus = gpus
        else:self.gpus = '0'
        if model_config:
            self.model_configs = model_config
        else:
            self.model_configs = '../bin/config/config_dabaigou.json'
            #self.model_configs = '../bin/config/config_godText_large1.json'
        self.predict_nums = 5
        self.tags = '(0)'
        self.rmHFW = False
        self.repetition_penalty = 1.2
        self.temperature = 0.6
        self.length = 30
        self.resort = True
        self.style = 'prose'
class config_predict1(Config):
    # 定义构造方法
    def __init__(self, model_config='', gpus=''):  # __init__() 是类的初始化方法；它在类的实例化操作后 会自动调用，不需要手动调用；
        super().__init__()
        if gpus:
            self.gpus = gpus
        else:self.gpus = '1'
        if model_config:
            self.model_configs = model_config
        else:
            self.model_configs = 'demo_config/config_dabaigou_small.json'
            #self.model_configs = '../bin/config/config_godText_large1.json'
        self.predict_nums = 5
        self.tags = '(1)'
        self.rmHFW = False
        self.repetition_penalty = 1.2
        self.temperature = 0.6
        self.length = 30
        self.resort = True
        self.style = 'prose'
class config_predict2(Config):
    # 定义构造方法
    def __init__(self, model_config='', gpus=''):  # __init__() 是类的初始化方法；它在类的实例化操作后 会自动调用，不需要手动调用；
        super().__init__()
        if gpus:
            self.gpus = gpus
        else:self.gpus = '0'
        if model_config:
            self.model_configs = model_config
        else:
            self.model_configs = 'demo_config/config_godText_small_finetune_merged_finetuneGodText.json'
            #self.model_configs = '../bin/config/config_godText_large1.json'
        self.predict_nums = 5
        self.tags = '(文)'
        self.rmHFW = False
        self.repetition_penalty = 1.2
        self.temperature = 0.6
        self.length = 30
        self.resort = True
        self.style = 'prose'

