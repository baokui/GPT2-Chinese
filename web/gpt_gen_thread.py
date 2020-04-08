#!/usr/bin/python3

import threading
import time
import numpy as np
import torch
from gpt_gen import generating,generating_poem
exitFlag = 0
class GPT2_generator_thread (threading.Thread):
    def __init__(self, threadID, name,
                 app,model,prefix,config,tokenizer,device,ConfigPredict,
                 quick,nsamples,removeHighFreqWords,batchGenerating,isPoem,tags='',gpu='0'):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.results = []
        self.app = app
        self.model = model
        self.prefix = prefix
        self.config = config
        self.tokenizer = tokenizer
        self.device = device
        self.ConfigPredict = ConfigPredict
        self.quick = quick
        self.nsamples = nsamples
        self.removeHighFreqWords = removeHighFreqWords
        self.batchGenerating = batchGenerating
        self.isPoem = isPoem
        self.tags = tags
        self.gpu = gpu
    def run(self):
        #print ("开始线程：" + self.name)
        #self.print_time(self.name, self.counter, 5)
        if not self.isPoem:
            self.results = self.generating_th(self.app, self.model, self.prefix, self.config, self.tokenizer, self.device, self.ConfigPredict,quick=self.quick, num=self.nsamples, removeHighFreqWords=self.removeHighFreqWords,batchGenerating=self.batchGenerating)
        else:
            self.results = self.generating_poem_th(self.app, self.model, self.prefix, self.config, self.tokenizer,
                                              self.device, self.ConfigPredict, quick=self.quick, num=self.nsamples,
                                              removeHighFreqWords=self.removeHighFreqWords,
                                              batchGenerating=self.batchGenerating)
        self.results = [rr+self.tags for rr in self.results]
        #print ("退出线程：" + self.name)
    def generating_th(self,app, model, prefix, config, tokenizer, device, ConfigPredict,
                   quick, num, removeHighFreqWords, batchGenerating):
        torch.cuda.set_device(int(self.gpu))
        S = generating(app, prefix, model, config, tokenizer, device, ConfigPredict,
                   quick, num, continue_writing = False,removeHighFreqWords=removeHighFreqWords, batchGenerating=batchGenerating,gpu=self.gpu)
        return S
    def generating_poem_th(self,app, model, prefix, config, tokenizer, device, ConfigPredict,
                   quick, num, removeHighFreqWords, batchGenerating):
        torch.cuda.set_device(int(self.gpu))
        S = generating_poem(app, prefix, model, config, tokenizer, device,
                   quick, num, batchGenerating,gpu=self.gpu)
        return S
def generating_thread(app,prefix, models, configs, tokenizers,devices,ConfigPredict,quick,nums,removeHighFreqWordss,batchGenerating,tags):
    nb_thread = len(models)
    Thread = []
    for t in range(nb_thread):
        if tags[t] == '(诗)':
            isPoem = True
        else:
            isPoem = False
        gpu = ConfigPredict.gpus[t]
        torch.cuda.set_device(int(gpu))
        thread1 = GPT2_generator_thread(t, "thread-"+str(t), app,models[t],prefix,configs[t],tokenizers[t],
                                        devices[t],ConfigPredict,quick,nums[t],
                                        removeHighFreqWordss[t],batchGenerating,isPoem,tags[t],gpu=gpu)
        Thread.append(thread1)
    #print('# 开启新线程')
    for th in Thread:
        th.start()
    #print('并行运行')
    for th in Thread:
        th.join()
    #print('运行结束')
    S = []
    for th in Thread:
        S.extend(th.results)
    return S
