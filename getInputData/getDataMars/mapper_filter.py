#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import random
import unicodedata
stopwords = [" ", "　", " ", ",", "，", ".", "。", "、", "!", "！", "?", "？", ";", "；", "~", "～", "·", "·", ".", "…", "-",
             "#_", "—", "+", "=", "'", "\"", "‘", "’", "“", "”", "*", "&", "^", "%", "$", "/", "\\", "@"]
punc_zh = "！？｡＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟‧﹏.…"
#punc_en = unicodedata.normalize('NFKC', punc_zh[:-1]) + unicodedata.normalize('NFKC', punc_zh[-1])[-1]
punc = ''.join(stopwords)+punc_zh
punc = punc.decode('utf-8')
app = 'com.tencent.mobileqq,com.tencent.mm,com.tencent.tim,com.sina.weibo,com.weico.international,com.weibo.international,com.taobao.taobao,com.taobao.taobao4iphone,com.wemomo.momoappdemo1,com.sogou.pandora.pandoralmClosedBeta,com.immomo.momo,com.sogou.xiaop_android,com.alibaba.android.rimet,com.laiwang.DingTalk,com.smile.gifmaker,com.jiangjia.gif,com.ss.android.ugc.aweme,com.ss.iphone.ugc.Aweme,com.bytedance.ee.lark,com.ss.android.lark,com.tencent.ww,com.tencent.wework,com.tencent.tim'
app = set(app.split(','))
def _is_chinese_char(char):
    """Checks whether CP is the codepoint of a CJK character."""
    # This defines a "chinese character" as anything in the CJK Unicode block:
    #   https://en.wikipedia.org/wiki/CJK_Unified_Ideographs_(Unicode_block)
    #
    # Note that the CJK Unicode block is NOT all Japanese and Korean characters,
    # despite its name. The modern Korean Hangul alphabet is a different block,
    # as is Japanese Hiragana and Katakana. Those alphabets are used to write
    # space-separated words, so they are not treated specially and handled
    # like the all of the other languages.
    cp = ord(char)
    if ((cp >= 0x4E00 and cp <= 0x9FFF) or  #
            (cp >= 0x3400 and cp <= 0x4DBF) or  #
            (cp >= 0x20000 and cp <= 0x2A6DF) or  #
            (cp >= 0x2A700 and cp <= 0x2B73F) or  #
            (cp >= 0x2B740 and cp <= 0x2B81F) or  #
            (cp >= 0x2B820 and cp <= 0x2CEAF) or
            (cp >= 0xF900 and cp <= 0xFAFF) or  #
            (cp >= 0x2F800 and cp <= 0x2FA1F)):  #
        return True
    return False
def _is_punc(char):
    if char in punc:
        return True
    return False
for line in sys.stdin:
    if random.uniform(0,1)<0.7:
        continue
    fields = line.strip().split('\t')
    if len(fields)!=5:
        continue
    if fields[2] not in app:
        continue
    s = fields[3].decode('utf-8')
    if len(s)<10 or len(s)>60:
        continue
    s_zh = [_is_chinese_char(char) for char in s]
    if len(s)<sum(s_zh)*0.7:
        continue
    s_punc = [_is_punc(char) for char in s]
    if sum(s_punc)>4:
        continue
    S = fields[3]
    sys.stdout.write("%s\n" % S)