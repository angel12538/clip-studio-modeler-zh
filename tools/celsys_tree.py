# -*- coding: utf-8 -*-
"""CELSYS 资源文件重建器 —— 终版

格式（已由 4 种语言样本 + 逐层验证确认）：
  任意节点 = [u32 子段数 N][N × {u32 id, u32 off, u32 len}]
    其中 off/len 精确覆盖子段区间，同层子段首尾相接无空隙
  叶子 = [u32 长度][UTF-8 文本]

改长度的正确做法：自底向上重建
  1. 递归收集所有叶子（字符串），按原顺序
  2. 用新文本重新排布叶子内容
  3. 自底向上重算每个节点的 off/len
"""
import struct, os, sys, glob

sys.stdout.reconfigure(encoding='utf-8')


def u32(b, p):
    return struct.unpack_from('>I', b, p)[0]


class Node:
    __slots__ = ('idx', 'start', 'length', 'children', 'is_leaf', 'text',
                 'start_out', 'length_out')

    def __init__(self, idx, start, length):
        self.idx = idx
        self.start = start
        self.length = length
        self.children = []
        self.is_leaf = False
        self.text = None


def parse_tree(b, start, length, idx=-1, depth=0):
    """解析节点。判定叶子：以 4 字节长度 + 恰好到边的 UTF-8 文本。"""
    node = Node(idx, start, length)
    if length < 4:
        node.is_leaf = True
        node.text = b[start:start + length].decode('utf-8', 'replace')
        return node

    # 先试叶子
    L = u32(b, start)
    if L > 0 and start + 4 + L == start + length:
        try:
            t = b[start + 4:start + 4 + L].decode('utf-8')
            if all(ord(c) >= 0x20 or c in '\t\n\r' for c in t):
                node.is_leaf = True
                node.text = t
                return node
        except UnicodeDecodeError:
            pass

    # 试内部节点
    if length >= 4:
        count = u32(b, start)
        if 0 < count <= 10000 and 4 + count * 12 <= length:
            p = start + 4
            ok = True
            kids = []
            expect = None
            for k in range(count):
                i = u32(b, p)
                o = u32(b, p + 4)
                ln = u32(b, p + 8)
                p += 12
                if o + ln > len(b) or ln > length:
                    ok = False
                    break
                if expect is not None and o != expect:
                    ok = False
                    break
                expect = o + ln
                kids.append((i, o, ln))
            if ok and kids:
                for i, o, ln in kids:
                    node.children.append(parse_tree(b, o, ln, i, depth + 1))
                return node

    # 都不匹配 —— 当作不透明数据，原样保留
    node.is_leaf = True
    node.text = None  # None 表示二进制原文
    return node


def collect_leaves(node, out):
    if node.is_leaf:
        out.append(node)
    else:
        for c in node.children:
            collect_leaves(c, out)
    return out


def build(b, root, new_texts):
    """new_texts: {leaf_序号: 新文本}。自底向上重算偏移。"""
    leaves = collect_leaves(root, [])
    # 1) 为每个叶子生成新内容
    leaf_bytes = {}
    for k, lf in enumerate(leaves):
        if lf.text is None:
            leaf_bytes[id(lf)] = b[lf.start:lf.start + lf.length]
            continue
        t = new_texts.get(k, lf.text)
        nb = t.encode('utf-8')
        leaf_bytes[id(lf)] = struct.pack('>I', len(nb)) + nb
    # 2) 自底向上：从根开始，先放子节点，再写自己
    out = bytearray()

    def emit(node):
        if node.is_leaf:
            data = leaf_bytes[id(node)]
            node.start_out = len(out)
            node.length_out = len(data)
            out.extend(data)
            return
        # 先给 header 占位
        header_pos = len(out)
        out.extend(b'\x00' * (4 + len(node.children) * 12))
        node.start_out = header_pos
        kids_info = []
        for c in node.children:
            emit(c)
            kids_info.append((c.idx, c.start_out, c.length_out))
        node.length_out = len(out) - header_pos
        # 回填 header
        struct.pack_into('>I', out, header_pos, len(node.children))
        for k, (i, o, ln) in enumerate(kids_info):
            struct.pack_into('>III', out, header_pos + 4 + k * 12, i, o, ln)

    emit(root)
    return bytes(out)


def roundtrip(path):
    b = open(path, 'rb').read()
    root = parse_tree(b, 0, len(b))
    out = build(b, root, {})
    ok = out == b
    nleaf = len(collect_leaves(root, []))
    return ok, len(b), len(out), nleaf


if __name__ == '__main__':
    base = sys.argv[1] if len(sys.argv) > 1 else \
        r'D:\Program Files\CELSYS\CLIP STUDIO 1.5\CLIP STUDIO MODELER\resource\english'
    print(f'目录: {base}\n')
    good = bad = 0
    for p in sorted(glob.glob(os.path.join(base, '*'))):
        name = os.path.basename(p)[:8]
        try:
            ok, s0, s1, nl = roundtrip(p)
        except Exception as e:
            print(f'  {name}  ERROR {e}')
            bad += 1
            continue
        if ok:
            good += 1
            print(f'  {name}  OK    size={s0:>8}  叶子={nl}')
        else:
            bad += 1
            print(f'  {name}  DIFF  {s0} -> {s1}   叶子={nl}')
    print(f'\n精确往返: {good}/{good + bad}')
