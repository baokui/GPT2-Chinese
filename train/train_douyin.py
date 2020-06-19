#-- coding:UTF-8 --
import transformers
import torch
import os
import json
import random
import numpy as np
import argparse
#from torch.utils.tensorboard import SummaryWriter
from datetime import datetime
from tqdm import tqdm
from torch.nn import DataParallel
from tokenizations.bpe_tokenizer import get_encoder
def iterData(path_data,rate=1.0,batch_size=32,epochs = 20):
    files = os.listdir(path_data)
    S = []
    for epoch in range(epochs):
        random.shuffle(files)
        for i in range(len(files)):
            f = open(os.path.join(path_data,files[i]),'r')
            for line in f:
                rate,line = line.split('\t')
                rate = float(rate)
                if random.uniform(0,1)>rate:
                    continue
                tokens = line.strip().split()
                tokens = [int(token) for token in tokens]
                S.append(tokens)
                if len(S)>=batch_size:
                    yield epoch,epochs,i,len(files),S
                    S = []
            f.close()
    yield '__STOP__'
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--device', default='0,1,2,3', type=str, required=False, help='设置使用哪些显卡')
    parser.add_argument('--model_config', default='config/model_config_small.json', type=str, required=False,
                        help='选择模型参数')
    parser.add_argument('--tokenizer_path', default='cache/vocab_small.txt', type=str, required=False, help='选择词库')
    parser.add_argument('--raw_data_path', default='data/train.json', type=str, required=False, help='原始训练语料')
    parser.add_argument('--tokenized_data_path', default='data/tokenized/', type=str, required=False,
                        help='tokenized语料存放位置')
    parser.add_argument('--raw', action='store_true', help='是否先做tokenize')
    parser.add_argument('--epochs', default=5, type=int, required=False, help='训练循环')
    parser.add_argument('--batch_size', default=64, type=int, required=False, help='训练batch size')
    parser.add_argument('--lr', default=1.5e-4, type=float, required=False, help='学习率')
    parser.add_argument('--warmup_steps', default=2000, type=int, required=False, help='warm up步数')
    parser.add_argument('--log_step', default=1, type=int, required=False, help='多少步汇报一次loss，设置为gradient accumulation的整数倍')
    parser.add_argument('--stride', default=768, type=int, required=False, help='训练时取训练数据的窗口步长')
    parser.add_argument('--gradient_accumulation', default=1, type=int, required=False, help='梯度积累')
    parser.add_argument('--fp16', action='store_true', help='混合精度')
    parser.add_argument('--fp16_opt_level', default='O1', type=str, required=False)
    parser.add_argument('--max_grad_norm', default=1.0, type=float, required=False)
    parser.add_argument('--num_pieces', default=100, type=int, required=False, help='将训练语料分成多少份')
    parser.add_argument('--min_length', default=128, type=int, required=False, help='最短收录文章长度')
    parser.add_argument('--max_length', default=256, type=int, required=False, help='最短收录文章长度')
    parser.add_argument('--output_dir', default='model/', type=str, required=False, help='模型输出路径')
    parser.add_argument('--pretrained_model', default='', type=str, required=False, help='模型训练起点路径')
    parser.add_argument('--writer_dir', default='tensorboard_summary/', type=str, required=False, help='Tensorboard路径')
    parser.add_argument('--segment', action='store_true', help='中文以词为单位')
    parser.add_argument('--bpe_token', action='store_true', help='subword')
    parser.add_argument('--encoder_json', default="tokenizations/encoder.json", type=str, help="encoder.json")
    parser.add_argument('--vocab_bpe', default="tokenizations/vocab.bpe", type=str, help="vocab.bpe")
    parser.add_argument('--max_steps_perEpoch_perPiece', default=1000000, type=int, required=False)
    parser.add_argument('--steps_savemodel', default=10000, type=int, required=False, help='保存模型步数')
    parser.add_argument('--padding', action='store_true', help='输入是否定长')
    args = parser.parse_args()
    print('args:\n' + args.__repr__())

    if args.segment:
        from tokenizations import tokenization_bert_word_level as tokenization_bert
    else:
        from tokenizations import tokenization_bert

    #os.environ["CUDA_VISIBLE_DEVICES"] = args.device  # 此处设置程序使用哪些显卡

    model_config = transformers.modeling_gpt2.GPT2Config.from_json_file(args.model_config)
    print('config:\n' + model_config.to_json_string())

    n_ctx = model_config.n_ctx
    if args.bpe_token:
        full_tokenizer = get_encoder(args.encoder_json, args.vocab_bpe)
    else:
        full_tokenizer = tokenization_bert.BertTokenizer(vocab_file=args.tokenizer_path)
    full_tokenizer.max_len = 999999
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print('using device:', device)

    raw_data_path = args.raw_data_path
    tokenized_data_path = args.tokenized_data_path
    raw = args.raw  # 选择是否从零开始构建数据集
    epochs = args.epochs
    batch_size = args.batch_size
    lr = args.lr
    warmup_steps = args.warmup_steps
    log_step = args.log_step
    stride = args.stride
    gradient_accumulation = args.gradient_accumulation
    fp16 = args.fp16  # 不支持半精度的显卡请勿打开
    fp16_opt_level = args.fp16_opt_level
    max_grad_norm = args.max_grad_norm
    num_pieces = args.num_pieces
    min_length = args.min_length
    output_dir = args.output_dir
    padding = args.padding
    max_length = args.max_length
    #tb_writer = SummaryWriter(log_dir=args.writer_dir)
    assert log_step % gradient_accumulation == 0
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    if not args.pretrained_model:
        model = transformers.modeling_gpt2.GPT2LMHeadModel(config=model_config)
    else:
        model = transformers.modeling_gpt2.GPT2LMHeadModel.from_pretrained(args.pretrained_model)
    model.train()
    model.to(device)

    num_parameters = 0
    parameters = model.parameters()
    for parameter in parameters:
        num_parameters += parameter.numel()
    print('number of parameters: {}'.format(num_parameters))
    multi_gpu = False
    optimizer = transformers.AdamW(model.parameters(), lr=lr, correct_bias=True)
    #scheduler = transformers.WarmupLinearSchedule(optimizer, warmup_steps=warmup_steps,
    #                                                      t_total=total_steps)
    if fp16:
        try:
            from apex import amp
        except ImportError:
            raise ImportError("Please install apex from https://www.github.com/nvidia/apex to use fp16 training.")
        model, optimizer = amp.initialize(model, optimizer, opt_level=fp16_opt_level)

    if torch.cuda.device_count() > 1:
        print("Let's use", torch.cuda.device_count(), "GPUs!")
        model = DataParallel(model, device_ids=[int(i) for i in args.device.split(',')])
        multi_gpu = True
    print('starting training')
    step_loss = 0
    running_loss = 10
    loss_ = 10
    iter = iterData(args.tokenized_data_path, rate=1.0, batch_size=batch_size, epochs=epochs)
    step = 0
    epoch0 = -1
    while True:
        data = next(iter)
        if data=='__STOP__':
            break
        epoch, epochs, idx_file, nb_files, batch_inputs = data
        random.shuffle(batch_inputs)
        batch_inputs = torch.tensor(batch_inputs).long().to(device)
        #  forward pass
        outputs = model.forward(input_ids=batch_inputs, labels=batch_inputs)
        loss, logits = outputs[:2]
        #  get loss
        if multi_gpu:
            loss = loss.mean()
        if gradient_accumulation > 1:
            loss = loss / gradient_accumulation
        #  loss backward
        if fp16:
            with amp.scale_loss(loss, optimizer) as scaled_loss:
                scaled_loss.backward()
                torch.nn.utils.clip_grad_norm_(amp.master_params(optimizer), max_grad_norm)
        else:
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_grad_norm)
        #  optimizer step
        if (step + 1) % gradient_accumulation == 0:
            running_loss += loss.item()
            optimizer.step()
            optimizer.zero_grad()
            step_loss += 1
            #scheduler.step()
        if (step + 1) % log_step == 0:
            loss_ = running_loss * gradient_accumulation / (log_step / gradient_accumulation)
            print('now time: {}:{}. step: {}, progress-innerEpoch: {}/{}, progress-outerEpoch: {}/{}, loss {}'.format(
                    datetime.now().hour,
                    datetime.now().minute,
                    step+1,
                    idx_file+1,
                    nb_files,
                    epoch + 1,
                    epochs,
                    loss_))
            running_loss = 0
        if step%args.steps_savemodel==0:
            print('saving model for epoch {}'.format(epoch + 1))
            output_dir_ = output_dir + 'model_epoch{}_step{}_loss-{}'.format(epoch + 1, step,'%0.2f'%loss_)
            if not os.path.exists(output_dir_):
                os.mkdir(output_dir_)
            model_to_save = model.module if hasattr(model, 'module') else model
            model_to_save.save_pretrained(output_dir_)
        step += 1
        if epoch!=epoch0:
            if not os.path.exists(output_dir + 'model_epoch{}'.format(epoch + 1)):
                os.mkdir(output_dir + 'model_epoch{}'.format(epoch + 1))
            model_to_save = model.module if hasattr(model, 'module') else model
            model_to_save.save_pretrained(output_dir + 'model_epoch{}'.format(epoch + 1))
            epoch0 = epoch
            print('epoch {} finished'.format(epoch + 1))
    if not os.path.exists(output_dir + 'final_model'):
        os.mkdir(output_dir + 'final_model')
    model_to_save = model.module if hasattr(model, 'module') else model
    model_to_save.save_pretrained(output_dir + 'final_model')
    print('training finished')

    # torch.save(scheduler.state_dict(), output_dir + 'final_model/scheduler.pt')
    # torch.save(optimizer.state_dict(), output_dir + 'final_model/optimizer.pt')


if __name__ == '__main__':
    main()
