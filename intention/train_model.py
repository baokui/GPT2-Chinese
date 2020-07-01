# coding: utf-8

from __future__ import print_function

import os
import sys
import time
from datetime import timedelta

import numpy as np
import tensorflow as tf

from rnn_model import TRNNConfig, TextRNN, Tokenizer
from data_loader import read_vocab, read_category, batch_iter,batch_iter_test, process_file, build_vocab,getTestData

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


def evaluate(sess, x_, y_):
    """评估在某一数据上的准确率和损失"""
    data_len = len(x_)
    batch_eval = batch_iter(x_, y_, 128)
    total_loss = 0.0
    total_acc = 0.0
    for x_batch, y_batch in batch_eval:
        batch_len = len(x_batch)
        feed_dict = feed_data(x_batch, y_batch, 1.0)
        y_pred_class, loss, acc = sess.run([model.y_pred_cls, model.loss, model.acc], feed_dict=feed_dict)
        total_loss += loss * batch_len
        total_acc += acc * batch_len
    return y_pred_class, total_loss / data_len, total_acc / data_len


def train():
    print("Configuring TensorBoard and Saver...")
    # 配置 Tensorboard，重新训练时，请将tensorboard文件夹删除，不然图会覆盖
    tf.summary.scalar("loss", model.loss)
    tf.summary.scalar("accuracy", model.acc)
    # 配置 Saver
    saver = tf.train.Saver()
    print("Loading training and validation data...")
    # 创建session
    session = tf.Session()
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    if not os.path.exists(ckpt_dir):
        session.run(tf.global_variables_initializer())
    else:
        ckpt = tf.train.latest_checkpoint(ckpt_dir)  # 找到存储变量值的位置
        saver.restore(session, ckpt)
        print('restore model from %s'%ckpt)
    print("Loading training and validation data...")
    # 载入训练集与验证集
    start_time = time.time()
    #x_train, y_train = process_file(train_dir, word_to_id, cat_to_id, config.seq_length)
    #x_val, y_val = process_file(val_dir, word_to_id, cat_to_id, config.seq_length)
    time_dif = get_time_dif(start_time)
    print("Time usage:", time_dif)
    print('Training and evaluating...')
    start_time = time.time()
    total_batch = 0  # 总批次
    best_acc_val = 0.0  # 最佳验证集准确率
    epoch0 = -1
    while True:
        batch_train = next(iter)
        if batch_train=='__STOP__':
            break
        epoch,x_batch, y_batch = batch_train
        if epoch0!=epoch:
            print('EPOCH: '+str(epoch))
            epoch0 = epoch
        feed_dict = feed_data(x_batch, y_batch, config.dropout_keep_prob,model)
        if total_batch % config.save_per_batch == 0:
            # 每多少轮次将训练结果写入tensorboard scalar
            #s = session.run(merged_summary, feed_dict=feed_dict)
            #writer.add_summary(s, total_batch)
            pass
        if total_batch % config.print_per_batch == 0:
            # 每多少轮次输出在训练集和验证集上的性能
            feed_dict[model.keep_prob] = 1.0
            loss_train, acc_train = session.run([model.loss, model.acc], feed_dict=feed_dict)
            x_test_batch, y_test_batch = next(iter_test)
            feed_dict_test = feed_data(x_test_batch, y_test_batch, config.dropout_keep_prob,model)
            feed_dict_test[model.keep_prob] = 1.0
            loss_val, acc_val = session.run([model.loss, model.acc], feed_dict=feed_dict_test)
            if acc_val > best_acc_val:
                # 保存最好结果
                best_acc_val = acc_val
                saver.save(sess=session, save_path=save_path)
            improved_str = 0.0
            time_dif = get_time_dif(start_time)
            msg = 'Iter: {0:>6}, Train Loss: {1:>6.2}, Train Acc: {2:>7.2%},' \
                  + ' Val Loss: {3:>6.2}, Val Acc: {4:>7.2%}, Time: {5} {6}'
            print(msg.format(total_batch, loss_train, acc_train, loss_val, acc_val, time_dif, improved_str))
        feed_dict[model.keep_prob] = config.dropout_keep_prob
        session.run(model.optim, feed_dict=feed_dict)  # 运行优化
        total_batch += 1

def test():
    # 配置 Saver
    saver = tf.train.Saver()
    #tensorboard_dir = 'tensorboard1/textrnn'
    print("Loading training and validation data...")
    ckpt = tf.train.latest_checkpoint(ckpt_dir)  # 找到存储变量值的位置
    # 创建session
    session = tf.Session()
    saver.restore(session, ckpt)
    #session.run(tf.global_variables_initializer())
    print('finish loading model!')
    print('predicting...')
    x, y, S = getTestData(predict_dir,tokenizer)
    feed_dict = feed_data(x, y, config.dropout_keep_prob, model)
    feed_dict[model.keep_prob] = 1.0
    modelpredict = tf.nn.softmax(model.logits)
    predict_y = session.run(modelpredict, feed_dict=feed_dict)
    predict_y = predict_y[:,0]
    T = [S[i]+'\t'+'%0.4f'%predict_y[i] for i in range(len(S))]
    with open(predict_dir.replace('predict','predict_result'),'w') as f:
        f.write('\n'.join(T))
    T = [[S[i],predict_y[i]] for i in range(len(S))]
    T = sorted(T,key=lambda x:-x[-1])
    T = ['\t'.join([t[0],str(t[1])]) for t in T]
    with open(predict_dir.replace('predict','predict_result_sorted'),'w') as f:
        f.write('\n'.join(T))
if __name__ == '__main__':
    base_dir = sys.argv[1]
    save_dir = sys.argv[2]
    ckpt_dir = sys.argv[3]
    train_dir = os.path.join(base_dir, 'train.txt')
    test_dir = os.path.join(base_dir, 'test.txt')
    val_dir = os.path.join(base_dir, 'val.txt')
    vocab_dir = os.path.join(base_dir, 'vocab.txt')
    predict_dir = os.path.join(base_dir, 'predict.txt')
    save_path = os.path.join(save_dir, 'best_validation')  # 最佳验证结果保存路径
    if len(sys.argv)>4:
        option = sys.argv[4]
    else:
        option = 'train'
    print('Configuring RNN model...')
    config = TRNNConfig()
    tokenizer = Tokenizer(vocab_dir)
    config.vocab_size = len(tokenizer.vocab)
    model = TextRNN(config)
    print('参数总量：%d'%np.sum([np.prod(v.get_shape().as_list()) for v in tf.trainable_variables()]))
    if option == 'train':
        iter = batch_iter(train_dir, tokenizer, epochs=config.num_epochs)
        iter_test = batch_iter_test(test_dir, tokenizer)
        train()
    else:
        test()
