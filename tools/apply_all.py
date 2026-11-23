# -*- coding: utf-8 -*-
"""一键汉化：把所有词表合并，应用到 resource\\chinese_tc。

用法：
    python tools/apply_all.py            # 预演，只统计不写入
    python tools/apply_all.py --apply    # 实际写入

前置条件：
    1. modeler15.txt 的语言标识已改为 chinese_tc（见 README）
    2. 原版 resource\\english\\ 保持完整
"""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config
from celsys_tree import parse_tree, collect_leaves, build

DRY = '--apply' not in sys.argv

HERE = os.path.dirname(os.path.abspath(__file__))


def load_dictionaries():
    """合并所有词表，返回 {英文: 中文}。后加载的覆盖先加载的。"""
    merged = {}

    # 1) 官方译文（底座）
    official_path = os.path.join(HERE, 'data', 'official_dict.json')
    if os.path.exists(official_path):
        try:
            with open(official_path, encoding='utf-8') as f:
                official = json.load(f).get('en2tc', {})
            merged.update(official)
            print('  官方译文       %5d 条' % len(official))
        except Exception as e:
            print('  [警告] 官方译文读取失败: %s' % e)

    # 2) 术语表
    try:
        from glossary import TERMS
        merged.update(TERMS)
        print('  术语表         %5d 条' % len(TERMS))
    except ImportError:
        print('  [警告] 未找到 glossary.py')

    # 3) 各批词表
    modules = [
        ('zh_short', 'ZH'),
        ('zh_mid1', 'ZH_MID_1'),
        ('zh_mid2', 'ZH_MID_2'),
        ('zh_batch3', 'ZH_BATCH3'),
        ('zh_batch4', 'ZH_BATCH4'),
        ('zh_batch5', 'ZH_BATCH5'),
        ('zh_batch6', 'ZH_BATCH6'),
        ('zh_batch7', 'ZH_BATCH7'),
        ('zh_batch8', 'ZH_BATCH8'),
        ('stage1_zh', 'STAGE1_ZH'),
        ('zh_extra', 'ZH_EXTRA'),
    ]
    for mod_name, var_name in modules:
        try:
            mod = __import__(mod_name)
            table = getattr(mod, var_name)
            merged.update(table)
            print('  %-14s %5d 条' % (mod_name + '.py', len(table)))
        except (ImportError, AttributeError) as e:
            print('  [跳过] %s: %s' % (mod_name, e))

    return merged


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


def apply_to_resources(dictionary):
    """把词典应用到全部资源文件，返回 (替换数, 叶子总数, 明细)。"""
    total_replaced = 0
    total_leaves = 0
    per_file = []

    if not DRY and not os.path.isdir(config.RESOURCE_CN):
        os.makedirs(config.RESOURCE_CN, exist_ok=True)
        print('  已创建 %s' % config.RESOURCE_CN)

    for name in sorted(os.listdir(config.RESOURCE_EN)):
        src = os.path.join(config.RESOURCE_EN, name)
        if not os.path.isfile(src):
            continue

        with open(src, 'rb') as f:
            raw = f.read()

        try:
            root = parse_tree(raw, 0, len(raw))
            leaves = collect_leaves(root, [])
        except Exception as e:
            print('  [跳过] %s 解析失败: %s' % (name[:8], e))
            continue

        total_leaves += sum(1 for lf in leaves
                            if lf.text and translatable(lf.text))

        mapping = {}
        for k, lf in enumerate(leaves):
            if not lf.text:
                continue
            zh = dictionary.get(lf.text)
            # 译文与原文相同视为未汉化，不计入替换
            if zh is not None and zh != lf.text:
                mapping[k] = zh

        if not mapping:
            out = raw
        else:
            out = build(raw, root, mapping)
            root2 = parse_tree(out, 0, len(out))
            leaves2 = collect_leaves(root2, [])
            bad = [k for k in mapping
                   if k >= len(leaves2) or leaves2[k].text != mapping[k]]
            if bad:
                print('  [失败] %s 有 %d 条校验不通过，跳过' % (name[:8], len(bad)))
                continue

        if not DRY:
            dst = os.path.join(config.RESOURCE_CN, name)
            try:
                with open(dst, 'wb') as f:
                    f.write(out)
            except PermissionError:
                print()
                print('错误：无法写入 %s' % dst)
                print('请先完全退出 CLIP STUDIO MODELER（含托盘图标）后重试。')
                sys.exit(1)
            except OSError as e:
                print()
                print('错误：写入 %s 失败（%s）' % (dst, e))
                print('若提示拒绝访问，请用管理员权限运行。')
                sys.exit(1)

        total_replaced += len(mapping)
        per_file.append((name[:8], len(mapping)))

    return total_replaced, total_leaves, per_file


def main():
    print('=' * 56)
    print(' CLIP STUDIO MODELER 简体中文汉化')
    print('=' * 56)
    print()
    print('模式：%s' % ('预演（不写入文件）' if DRY else '实际写入'))
    print()

    config.require_modeler()
    config.describe()
    print()

    print('加载词表：')
    dictionary = load_dictionaries()
    print('  %-14s %5d 条（合并后）' % ('合计', len(dictionary)))
    print()

    print('应用到资源文件：')
    replaced, leaves, per_file = apply_to_resources(dictionary)
    print()

    if per_file:
        print('%-12s %s' % ('文件', '替换条数'))
        print('-' * 24)
        for n, c in sorted(per_file, key=lambda x: -x[1])[:12]:
            print('%-12s %d' % (n, c))
        if len(per_file) > 12:
            print('... 其余 %d 个文件' % (len(per_file) - 12))
        print()

    print('=' * 56)
    print(' 总叶子数  : %d' % leaves)
    print(' 已替换    : %d' % replaced)
    if leaves:
        print(' 覆盖率    : %.1f%%' % (100.0 * replaced / leaves))
    print('=' * 56)

    if DRY:
        print()
        print('这是预演。加 --apply 参数实际写入。')
    else:
        print()
        print('完成。请重新启动 CLIP STUDIO MODELER。')
        print('若界面未变化，检查 modeler15.txt 语言标识是否为 chinese_tc。')


if __name__ == '__main__':
    main()
