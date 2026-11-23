# -*- coding: utf-8 -*-
"""重新生成 official_dict.json 的完整流程。

步骤：
  1. 从 .bak-t2s 恢复（该版本已转简体字形，但含台湾词汇）
  2. tw2sp 二次转换（补上 t2s 漏掉的词汇差异）
  3. 术语纠正（组件→元件、缺省→默认、位图→点阵）
  4. 台湾用语词汇纠正（档案→文件、记忆体→内存…）

关键教训：
  - 「预设」= preset，大陆同样用「预设」，不能改成「默认」（=default）
  - 必须先 tw2sp 再词汇纠正，顺序反了会丢词汇信息
"""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

LIB = r'C:\Users\Administrator\Documents\CSP-简体中文补丁\tools\libs'
sys.path.insert(0, LIB)

from opencc import OpenCC
from taiwan_words import normalize

tw2sp = OpenCC('tw2sp')
t2s = OpenCC('t2s')

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, 'data', 'official_dict.json')
BAK = PATH + '.bak-t2s'

# 术语纠正（tw2sp 过度转换的部分）
TERM_FIX = [('组件', '元件'), ('缺省', '默认'), ('位图', '点阵')]


def term_fix(s):
    for a, b in TERM_FIX:
        s = s.replace(a, b)
    return s


# 1) 恢复
if not os.path.exists(BAK):
    print('错误：找不到备份 %s' % BAK)
    sys.exit(1)
with open(BAK, encoding='utf-8') as f:
    base = json.load(f)['en2tc']
print('[1] 从备份恢复 %d 条' % len(base))

# 2) tw2sp
out = {}
n_tw = 0
for k, v in base.items():
    nv = tw2sp.convert(v)
    if nv != v:
        n_tw += 1
    out[k] = nv
print('[2] tw2sp 转换 %d 条' % n_tw)

# 3) 术语纠正
n_term = 0
for k, v in out.items():
    nv = term_fix(v)
    if nv != v:
        n_term += 1
    out[k] = nv
print('[3] 术语纠正 %d 条' % n_term)

# 4) 台湾用语纠正
n_word = 0
for k, v in out.items():
    nv = normalize(v)
    if nv != v:
        n_word += 1
    out[k] = nv
print('[4] 台湾用语纠正 %d 条' % n_word)

# 校验：不应再有繁体字形
residual = [(k, v) for k, v in out.items() if t2s.convert(v) != v]
print()
print('[校验] 繁体字形残留 %d 条' % len(residual))
for k, v in residual[:5]:
    print('  %r' % v[:60])

tmp = PATH + '.tmp'
with open(tmp, 'w', encoding='utf-8') as f:
    json.dump({'en2tc': out}, f, ensure_ascii=False, separators=(',', ':'))
os.replace(tmp, PATH)
print()
print('已写入（%d 字节）' % os.path.getsize(PATH))

# 关键样例抽查
print()
print('=== 关键样例 ===')
CHECK = {
    'Material preset': '应含「预设」',
    'Angle preset': '应含「预设」',
    'Quit': '退出',
    'Apply': '应用',
    'Customize': '自定义',
    'Failed to upload the file.': '文件',
}
for k, note in CHECK.items():
    if k in out:
        print('  %-32r -> %r   (%s)' % (k[:30], out[k][:40], note))
