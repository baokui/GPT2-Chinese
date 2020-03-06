import sys
import random
idx = list('012345')
for line in sys.stdin:
    fields = line.strip().split('\t')
    if len(fields)!=5:
        continue
    s = fields[3].decode('utf-8')
    if len(s)<10 or len(s)>60:
        continue
    random.shuffle(idx)
    Id = ''.join(idx)
    S = Id+'\t'+fields[3]
    sys.stdout.write("%s\n" % S)