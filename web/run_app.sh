port=5000
nohup /root/anaconda3/envs/pytorch/bin/python3.6 app.py $port >> log/$port.log 2>&1 &
port=5001
nohup /root/anaconda3/envs/pytorch/bin/python3.6 app_nnlm.py $port >> log/$port.log 2>&1 &
#port=5002
#nohup python app.py $port >> log/$port.log 2>&1 &
