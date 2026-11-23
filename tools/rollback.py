# -*- coding: utf-8 -*-
"""还原为英文原版。

用法：
    python tools/rollback.py            # 预演
    python tools/rollback.py --apply    # 实际执行

做三件事：
    1. 删除 resource\\chinese_tc\\
    2. 用反向词典把材质标签改回英文
    3. 提示手动修改 modeler15.txt 的语言标识

注意：删除 chinese_tc 后若要恢复汉化，重跑 apply_all.py 即可。
      材质标签的还原不依赖备份文件，用的是词表反向映射。
"""
import os
import sys
import shutil
import sqlite3

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config
from tags_zh import TAG_ZH, SYSTEMTAG_ZH, FOLDERTAG_ZH

DRY = '--apply' not in sys.argv

# 反向映射：中文 -> 英文
TAG_EN = {v: k for k, v in TAG_ZH.items()}
SYSTEMTAG_EN = {v: k for k, v in SYSTEMTAG_ZH.items()}
FOLDERTAG_EN = {v: k for k, v in FOLDERTAG_ZH.items()}


def remove_chinese_resource():
    if not config.RESOURCE_CN or not os.path.isdir(config.RESOURCE_CN):
        print('  chinese_tc 不存在，跳过')
        return
    n = len(os.listdir(config.RESOURCE_CN))
    print('  将删除 %s（%d 个文件）' % (config.RESOURCE_CN, n))
    if not DRY:
        shutil.rmtree(config.RESOURCE_CN)
        print('  已删除')


def revert_tags():
    """用反向词典把材质标签改回英文。"""
    if not config.CMDB or not os.path.exists(config.CMDB):
        print('  未找到材质数据库，跳过')
        return

    c = sqlite3.connect(config.CMDB)
    cur = c.cursor()
    n = 0
    for table, mapping in (('Tag', TAG_EN),
                           ('SystemTag', SYSTEMTAG_EN),
                           ('FolderTag', FOLDERTAG_EN)):
        try:
            cur.execute('SELECT _PW_ID, Title FROM "%s"' % table)
            rows = cur.fetchall()
        except sqlite3.Error:
            continue
        for rid, title in rows:
            if title in mapping:
                if not DRY:
                    cur.execute('UPDATE "%s" SET Title=? WHERE _PW_ID=?'
                                % table, (mapping[title], rid))
                n += 1
    if not DRY:
        c.commit()
    c.close()
    print('  数据库恢复 %d 行' % n)

    # info.xml 反向替换
    if not config.MATERIAL_ROOT or not os.path.isdir(config.MATERIAL_ROOT):
        return
    n_file = n_tag = 0
    for dirpath, _, names in os.walk(config.MATERIAL_ROOT):
        if 'info.xml' not in names:
            continue
        path = os.path.join(dirpath, 'info.xml')
        try:
            with open(path, 'r', encoding='utf-8') as f:
                raw = f.read()
        except OSError:
            continue
        hit = False
        for zh, en in TAG_EN.items():
            token = '<data>%s</data>' % zh
            if token in raw:
                raw = raw.replace(token, '<data>%s</data>' % en)
                hit = True
                n_tag += 1
        if hit:
            n_file += 1
            if not DRY:
                with open(path, 'w', encoding='utf-8', newline='') as f:
                    f.write(raw)
    print('  info.xml 恢复 %d 个文件 / %d 处' % (n_file, n_tag))


def main():
    print('=' * 56)
    print(' 还原为英文原版')
    print('=' * 56)
    print()
    print('模式：%s' % ('预演' if DRY else '实际执行'))
    print()

    if config.MODELER_DIR:
        config.describe()
        print()
    else:
        print('提示：未找到 MODELER 安装目录，仅处理材质标签。')
        print()

    print('[1] 中文资源文件')
    remove_chinese_resource()
    print()

    print('[2] 材质标签')
    revert_tags()
    print()

    print('[3] 语言标识')
    print('  需手动把以下文件中的 "Language" 改为 "english"：')
    print(r'  C:\ProgramData\CELSYS\CLIPStudio\InstallPath\modeler15.txt')
    print('  （该文件 ACL 较严，通常需用管理员权限的记事本编辑）')
    print()

    print('=' * 56)
    if DRY:
        print(' 预演完毕。加 --apply 实际执行。')
    else:
        print(' 还原完成。请重启 CLIP STUDIO MODELER。')
    print('=' * 56)


if __name__ == '__main__':
    main()
