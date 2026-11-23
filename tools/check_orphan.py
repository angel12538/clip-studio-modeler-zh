# -*- coding: utf-8 -*-
"""一致性检查：磁盘上的中文资源，有无词表覆盖不到的残留译文。"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config
from celsys_tree import parse_tree, collect_leaves

# 复用 apply_all 的词表加载
import importlib
apply_mod = importlib.import_module('apply_all')
DICT = apply_mod.load_dictionaries()


def has_cjk(s):
    return any('\u4e00' <= c <= '\u9fff' for c in s)


total = 0
cjk = 0
changed = 0
orphan = []

for name in sorted(os.listdir(config.RESOURCE_EN)):
    en_p = os.path.join(config.RESOURCE_EN, name)
    cn_p = os.path.join(config.RESOURCE_CN, name)
    if not os.path.exists(cn_p):
        continue
    with open(en_p, 'rb') as f:
        b_en = f.read()
    with open(cn_p, 'rb') as f:
        b_cn = f.read()
    le = [x.text for x in collect_leaves(parse_tree(b_en, 0, len(b_en)), [])]
    lc = [x.text for x in collect_leaves(parse_tree(b_cn, 0, len(b_cn)), [])]
    if len(le) != len(lc):
        print('[不一致] %s 叶子数 %d vs %d' % (name[:8], len(le), len(lc)))
        continue
    for a, c in zip(le, lc):
        if not a or not apply_mod.translatable(a):
            continue
        total += 1
        if has_cjk(c):
            cjk += 1
        if a != c:
            changed += 1
            # 这条变了，但词表里没有对应项？
            if a not in DICT:
                orphan.append((name[:8], a, c))

print()
print('可翻译叶子   : %d' % total)
print('含中文的     : %d' % cjk)
print('与英文不同的 : %d' % changed)
print('词表外的残留 : %d' % len(orphan))
if orphan:
    print()
    for f, a, c in orphan[:20]:
        print('  %s  %r -> %r' % (f, a[:40], c[:40]))
