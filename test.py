from generate import *
from tokenizations import tokenization_bert

os.environ["CUDA_VISIBLE_DEVICES"] = "0"  # 此处设置程序使用哪些显卡
tokenizer_path = "./model/gpt2_prose/vocab.txt"
model_config = "./model/model_godText/final_model/config.json"
model_path = "./model/model_godText/final_model/"
save_samples_path = "./test_godText/finetuned/"
length = 50
batch_size = 4
nsamples = 10
temperature = 1.0
topk = 8
topp = 0
repetition_penalty = 1.0
device = 'cpu'
tokenizer = tokenization_bert.BertTokenizer(vocab_file=tokenizer_path)
model = GPT2LMHeadModel.from_pretrained(model_path)
model.to(device)
model.eval()

params = list(model.parameters())
k = 0
for i in params:
    l = 1
    #print("该层的结构：" + str(list(i.size())))
    for j in i.size():
        l *= j
    #print("该层参数和：" + str(l))
    k = k + l
print("总参数数量和:%dM"%int(k/1024/1024))

n_ctx = model.config.n_ctx

if length == -1:
    length = model.config.n_ctx
prefix = "今天天气真好"
nsamples = 3
temperature = 0.2
def main(prefix,temperature,length,topk,topp,nsamples=5):
    raw_text = prefix
    context_tokens = tokenizer.convert_tokens_to_ids(tokenizer.tokenize(raw_text))
    generated = 0
    for _ in range(nsamples):
        out = generate(
            n_ctx=n_ctx,
            model=model,
            context=context_tokens,
            length=length,
            is_fast_pattern=True, tokenizer=tokenizer,
            temperature=temperature, top_k=topk, top_p=topp, repitition_penalty=repetition_penalty, device=device
        )
        generated += 1
        text = tokenizer.convert_ids_to_tokens(out)
        for i, item in enumerate(text[:-1]):  # 确保英文前后有空格
            if is_word(item) and is_word(text[i + 1]):
                text[i] = item + ' '
        for i, item in enumerate(text):
            if item == '[MASK]':
                text[i] = ''
            elif item == '[CLS]':
                text[i] = '\n\n'
            elif item == '[SEP]':
                text[i] = '\n'
        info = "=" * 40 + " SAMPLE " + str(generated) + " " + "=" * 40 + "\n"
        print(info)
        text = ''.join(text).replace('##', '').strip()
        # print(text)
        print(text)

