import sys
import random
idx = list('012345')
app = 'com.tencent.mobileqq,com.tencent.mm,com.tencent.tim,com.sina.weibo,com.weico.international,com.weibo.international,com.taobao.taobao,com.taobao.taobao4iphone,com.wemomo.momoappdemo1,com.sogou.pandora.pandoralmClosedBeta,com.immomo.momo,com.sogou.xiaop_android,com.alibaba.android.rimet,com.laiwang.DingTalk,com.smile.gifmaker,com.jiangjia.gif,com.ss.android.ugc.aweme,com.ss.iphone.ugc.Aweme,com.bytedance.ee.lark,com.ss.android.lark,com.tencent.ww,com.tencent.wework,com.tencent.tim'
app = set(app.split(','))
for line in sys.stdin:
    fields = line.strip().split('\t')
    if len(fields)!=5:
        continue
    if fields[2] not in app:
        continue
    s = fields[3].decode('utf-8')
    if len(s)<10 or len(s)>60:
        continue
    random.shuffle(idx)
    Id = ''.join(idx)
    S = Id+'\t'+fields[3]
    sys.stdout.write("%s\n" % S)