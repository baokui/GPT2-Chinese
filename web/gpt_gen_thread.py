#!/usr/bin/python3

import threading
import time
import numpy as np
import torch
from gpt_gen import generating,generating_poem,nnlm_modelpredict
exitFlag = 0
class GPT2_generator_thread (threading.Thread):
    def __init__(self, threadID, name,
                 app,model,prefix,config,tokenizer,device,ConfigPredict,
                 quick,nsamples,removeHighFreqWords,batchGenerating,isPoem=False,tags='',gpu='0',
                 nnlm=False,D_simi={},D_next={},maxNext=3,maxChoice=10,onlyMax=False):
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
        self.nnlm = nnlm
        self.D_simi = D_simi
        self.D_next = D_next
        self.maxNext = maxNext
        self.maxChoice = maxChoice
        self.onlyMax = onlyMax
    def run(self):
        #print ("开始线程：" + self.name)
        #self.print_time(self.name, self.counter, 5)
        if self.nnlm:
            self.results = self.generating_nnlm_th(self.D_simi,self.D_next,self.ConfigPredict,self.prefix,self.maxNext,self.maxChoice,self.nsamples)
        else:
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
                   quick, num, continue_writing = False,removeHighFreqWords=removeHighFreqWords,
                       batchGenerating=batchGenerating,gpu=self.gpu,onlyMax=self.onlyMax)
        return S
    def generating_poem_th(self,app, model, prefix, config, tokenizer, device, ConfigPredict,
                   quick, num, removeHighFreqWords, batchGenerating):
        torch.cuda.set_device(int(self.gpu))
        S = generating_poem(app, prefix, model, config, tokenizer, device,
                   quick, num, batchGenerating,gpu=self.gpu,onlyMax=self.onlyMax,fast_pattern=ConfigPredict.fast_pattern)
        return S
    def generating_nnlm_th(self,D_simi,D_next,ConfigPredict,inputStr,maxNext,maxChoice,num):
        result_nnlm = nnlm_modelpredict(D_simi,D_next,ConfigPredict,inputStr=inputStr,maxNext=maxNext,maxChoice=maxChoice,num=num)
        return result_nnlm
def generating_thread(app,prefix, models, configs, tokenizers,devices,ConfigPredict,quick,nums,removeHighFreqWordss,batchGenerating,tags,D_simi={},D_next={},maxNext=3,maxChoice=10,onlyMax=False):
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
                                        removeHighFreqWordss[t],batchGenerating,isPoem,tags[t],gpu=gpu,onlyMax=onlyMax)
        Thread.append(thread1)
    t = nb_thread
    thread2 = GPT2_generator_thread(t, "thread-"+str(t), app,models[t-1],prefix,configs[t-1],tokenizers[t-1],
                                        devices[t-1],ConfigPredict,quick,nums[t],
                                        removeHighFreqWordss[t-1],batchGenerating=False,tags=tags[t],nnlm=True,D_simi=D_simi,D_next=D_next,maxNext=maxNext,maxChoice=maxChoice)
    Thread.append(thread2)
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
