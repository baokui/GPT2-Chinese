# coding: utf-8

from __future__ import print_function

import os
import sys
import time
from datetime import timedelta
from rnn_model import TRNNConfig, TextRNN, Tokenizer
import numpy as np
import tensorflow as tf
from flask import Flask, request, Response
from gevent.pywsgi import WSGIServer
from gevent import monkey
import random
import json
import logging
monkey.patch_all()
app = Flask(__name__)

max_len = 10
base_dir = sys.argv[1]
save_dir = sys.argv[2]
vocab_dir = os.path.join(base_dir, 'vocab.txt')
save_path = os.path.join(save_dir, 'best_validation')
config = TRNNConfig()
tokenizer = Tokenizer(vocab_dir)
config.vocab_size = len(tokenizer.vocab)
model = TextRNN(config)
#print('参数总量：%d'%np.sum([np.prod(v.get_shape().as_list()) for v in tf.trainable_variables()]))
saver = tf.train.Saver()
ckpt = tf.train.latest_checkpoint(save_dir)  # 找到存储变量值的位置
# 创建session
session = tf.Session()
saver.restore(session, ckpt)
def get_time_dif(start_time):
    """获取已使用时间"""
    end_time = time.time()
    time_dif = end_time - start_time
    return timedelta(seconds=int(round(time_dif)))
def feed_data(x_batch, y_batch, keep_prob,model):
    feed_dict = {
        model.input_x: x_batch,
        model.input_y: y_batch,
        model.keep_prob: keep_prob
    }
    return feed_dict
@app.route('/api/intention', methods=['POST'])
def test():
    r = request.json
    inputStr = r["input"]
    #inputStr = '想你'
    x = [tokenizer.tokenization(inputStr[-max_len:], max_len=max_len)]
    y = [[1, 0]]
    feed_dict = feed_data(x, y, config.dropout_keep_prob, model)
    feed_dict[model.keep_prob] = 1.0
    modelpredict = tf.nn.softmax(model.logits)
    predict_y = session.run(modelpredict, feed_dict=feed_dict)
    predict_y = predict_y[:,0]
    response = {'message': 'success', 'input': inputStr, 'result': predict_y}
    response_pickled = json.dumps(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")
if __name__ == '__main__':
    test()

