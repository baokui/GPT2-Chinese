from generate1 import generating
def main(config_pretrain,config_finetune,path_text):
    with open(path_text,'r') as f:
        s = f.read().strip().split('\n')
    generating(config_pretrain,s)
    generating(config_finetune,s)

