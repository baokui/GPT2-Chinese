mkdir log
nohup python -u train_model.py data2 checkpoints2/textrnn checkpoints1/textrnn >> log/train.log 2>&1 &
nohup python -u train_model.py data2 checkpoints2/textrnn checkpoints1/textrnn predict >> log/test.log 2>&1 &