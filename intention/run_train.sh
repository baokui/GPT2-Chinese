mkdir log
base_dir="data2"
save_dir="checkpoints2/textrnn"
ckpt_dir="checkpoints1/textrnn"
nohup python -u train_model.py data2 checkpoints2/textrnn checkpoints1/textrnn >> log/train.log 2>&1 &
nohup python -u train_model.py data2 checkpoints2/textrnn checkpoints1/textrnn predict >> log/test.log 2>&1 &