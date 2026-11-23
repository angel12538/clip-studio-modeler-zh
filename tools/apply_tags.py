# -*- coding: utf-8 -*-
"""材质标签汉化：数据库三张表 + 每个素材的 info.xml。

用法：
    python tools/apply_tags.py            # 预演
    python tools/apply_tags.py --apply    # 实际写入

注意：执行前请先退出 CLIP STUDIO MODELER，
      否则程序内存中的旧标签会覆盖磁盘改动，重启后不生效。
"""
import os
import sys
import sqlite3

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config
from tags_zh import TAG_ZH, SYSTEMTAG_ZH, FOLDERTAG_ZH

DRY = '--apply' not in sys.argv


def apply_database():
    """改写数据库三张表。"""
    if not config.CMDB or not os.path.exists(config.CMDB):
        print('  未找到材质数据库，跳过')
        return 0

    c = sqlite3.connect(config.CMDB)
    cur = c.cursor()
    changed = 0

    for table, mapping in (('Tag', TAG_ZH),
                           ('SystemTag', SYSTEMTAG_ZH),
                           ('FolderTag', FOLDERTAG_ZH)):
        try:
            cur.execute('SELECT _PW_ID, Title FROM "%s"' % table)
            rows = cur.fetchall()
        except sqlite3.Error as e:
            print('  [警告] 读取 %s 失败: %s' % (table, e))
            continue

        print('  %s（%d 行）' % (table, len(rows)))
        for rid, title in rows:
            if title in mapping:
                new = mapping[title]
                print('    %3d  %s -> %s' % (rid, repr(title), repr(new)))
                if not DRY:
                    cur.execute('UPDATE "%s" SET Title=? WHERE _PW_ID=?'
                                % table, (new, rid))
                changed += 1

    if not DRY:
        c.commit()
    c.close()
    return changed


def apply_info_xml():
    """改写素材 info.xml 里的标签。"""
    if not config.MATERIAL_ROOT or not os.path.isdir(config.MATERIAL_ROOT):
        print('  未找到素材目录，跳过')
        return 0, 0

    files = []
    for dirpath, _, names in os.walk(config.MATERIAL_ROOT):
        if 'info.xml' in names:
            files.append(os.path.join(dirpath, 'info.xml'))

    n_file = n_tag = 0
    for path in files:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                raw = f.read()
        except OSError:
            continue

        hit = False
        for en, zh in TAG_ZH.items():
            token = '<data>%s</data>' % en
            if token in raw:
                raw = raw.replace(token, '<data>%s</data>' % zh)
                hit = True
                n_tag += 1
        if hit:
            n_file += 1
            if not DRY:
                with open(path, 'w', encoding='utf-8', newline='') as f:
                    f.write(raw)

    return n_file, n_tag


def main():
    print('=' * 56)
    print(' 材质标签汉化')
    print('=' * 56)
    print()
    print('模式：%s' % ('预演（不写入）' if DRY else '实际写入'))
    print()

    if not config.USERDATA:
        print('错误：找不到 CELSYS 用户数据目录。')
        print('材质标签存放在用户数据目录下，需先运行一次 MODELER 生成。')
        sys.exit(1)

    print('数据库：')
    n_db = apply_database()
    print('  更新 %d 行' % n_db)
    print()

    print('素材 info.xml：')
    n_file, n_tag = apply_info_xml()
    print('  %d 个文件，%d 处标签' % (n_file, n_tag))
    print()

    print('=' * 56)
    if DRY:
        print(' 预演完毕。加 --apply 实际执行。')
    else:
        print(' 完成。请重启 CLIP STUDIO MODELER 查看效果。')
    print('=' * 56)


if __name__ == '__main__':
    main()
