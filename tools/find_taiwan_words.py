# -*- coding: utf-8 -*-
"""查找「详细资讯」等台湾用语残留的来源。"""
import os
import sys
import importlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config
from celsys_tree import parse_tree, collect_leaves

apply_mod = importlib.import_module('apply_all')
DICT = apply_mod.load_dictionaries()

# 台湾用语特征词（词汇级，非字符级）
TAIWAN_WORDS = ['资讯', '程式', '滑鼠', '伺服器', '网路', '软体', '硬体',
                '档案', '资料', '预设', '选单', '记忆体', '讯息', '检视']

print('=== 含台湾用语的字符串（界面文本）===\n')
found = {}
for name in sorted(os.listdir(config.RESOURCE_CN)):
    p = os.path.join(config.RESOURCE_CN, name)
    if not os.path.isfile(p):
        continue
    with open(p, 'rb') as f:
        b = f.read()
    try:
        leaves = collect_leaves(parse_tree(b, 0, len(b)), [])
    except Exception:
        continue
    for lf in leaves:
        t = lf.text
        if not t or len(t) > 200:
            continue
        for w in TAIWAN_WORDS:
            if w in t:
                found.setdefault(t, (name[:8], w))
                break

for t, (f, w) in sorted(found.items(), key=lambda x: len(x[0])):
    print('  [%s] %-46r (%s)' % (w, t[:44], f))

print()
print('共 %d 条' % len(found))
