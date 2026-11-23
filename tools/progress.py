# -*- coding: utf-8 -*-
"""汉化进度统计：统计 chinese_tc 相对 english 的汉化覆盖率。"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config
from celsys_tree import parse_tree, collect_leaves


def translatable(t):
    """判断是否属于应当翻译的文本（排除格式名、代码等）。"""
    if not t or len(t.strip()) < 2:
        return False
    if not any(c.isascii() and c.isalpha() for c in t):
        return False
    bad = ('://', '\\', 'GL_', 'gl_', '#version', 'uniform ', 'varying ',
           'void main', 'vec2 ', 'vec3 ', 'vec4 ', 'float4 ', 'sampler2D')
    if any(b in t for b in bad):
        return False
    if len(t) > 800:
        return False
    return True


def has_cjk(s):
    return any('\u4e00' <= c <= '\u9fff' for c in s)


def main():
    config.require_modeler()

    if not os.path.isdir(config.RESOURCE_CN):
        print('chinese_tc 目录不存在，尚未汉化。')
        print('请先运行：python tools/apply_all.py --apply')
        return

    total = done = 0
    per_file = []

    for name in sorted(os.listdir(config.RESOURCE_EN)):
        en_path = os.path.join(config.RESOURCE_EN, name)
        cn_path = os.path.join(config.RESOURCE_CN, name)
        if not os.path.isfile(en_path) or not os.path.exists(cn_path):
            continue

        try:
            with open(en_path, 'rb') as f:
                b_en = f.read()
            with open(cn_path, 'rb') as f:
                b_cn = f.read()
            le = [x.text for x in collect_leaves(parse_tree(b_en, 0, len(b_en)), [])]
            lc = [x.text for x in collect_leaves(parse_tree(b_cn, 0, len(b_cn)), [])]
        except Exception as e:
            print('  [跳过] %s: %s' % (name[:8], e))
            continue

        if len(le) != len(lc):
            print('  [警告] %s 叶子数不一致 %d vs %d' % (name[:8], len(le), len(lc)))
            continue

        f_total = f_done = 0
        for a, c in zip(le, lc):
            if not translatable(a):
                continue
            f_total += 1
            if has_cjk(c) or a != c:
                f_done += 1

        total += f_total
        done += f_done
        if f_total:
            per_file.append((name[:8], f_total, f_done))

    print('=' * 52)
    print(' 汉化进度')
    print('=' * 52)
    print(' 可翻译叶子 : %d' % total)
    print(' 已汉化     : %d' % done)
    if total:
        print(' 覆盖率     : %.1f%%' % (100.0 * done / total))
    print('=' * 52)

    if per_file:
        print()
        print('%-12s %8s %8s %8s' % ('文件', '总数', '已汉化', '覆盖率'))
        print('-' * 40)
        for n, t, d in sorted(per_file, key=lambda x: -(x[1] - x[2])):
            print('%-12s %8d %8d %7.1f%%' % (n, t, d, 100.0 * d / t))


if __name__ == '__main__':
    main()
