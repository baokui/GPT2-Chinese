import logging
from distiller.data_loggers import *
import DataLoader
import distiller.apputils.image_classifier as ic
import torch
from distiller.quantization.range_linear import PostTrainLinearQuantizer
from opt import args
import distiller.apputils as apputils
from distiller.apputils.image_classifier import test
import torch.nn as nn
import os
from transformers import GPT2LMHeadModel

model_path = 'model/tmpfile/'

model = GPT2LMHeadModel.from_pretrained(model_path)
model.load_state_dict(model_path)

model = model.cuda()
model.eval()

quantizer = PostTrainLinearQuantizer(model)

quantizer.prepare_model(torch.rand([你的模型输入的大小如[1, 3, 32, 32]]))

apputils.save_checkpoint(0, 'my_model', model, optimizer=None,
                         name='quantized',
                         dir='model/tmpfile_quantization')