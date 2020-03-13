import sys
import jieba
for data in sys.stdin:
    data = data.strip()
    fields = data.split('\t')
    if len(fields) != 2:
        continue
    sent = jieba.cut(fields[1])
    words = ' '.join([ele.encode("utf-8") for ele in sent])
    S = '\t'.join([fields[0],words])
    sys.stdout.write("%s\n" % S)

