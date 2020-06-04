mkdir log
nohup python -u train_model.py data1 checkpoints1/textrnn >> log/train.log 2>&1 &