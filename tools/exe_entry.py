# -*- coding: utf-8 -*-
"""exe 入口：把汉化流程整合成双击即用的单个程序。

打包命令见 build_exe.bat。
"""
import os
import sys

# ---------- 控制台编码：确保中文正常显示 ----------
if sys.platform == 'win32':
    try:
        import ctypes
        ctypes.windll.kernel32.SetConsoleOutputCP(65001)
        ctypes.windll.kernel32.SetConsoleCP(65001)
    except Exception:
        pass
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# ---------- 资源路径：兼容 PyInstaller 打包 ----------
if getattr(sys, 'frozen', False):
    BASE = sys._MEIPASS          # 打包后的临时解压目录
else:
    BASE = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, BASE)

import importlib
from celsys_tree import parse_tree, collect_leaves, build

# ---------- 静态导入词表模块 ----------
# 这些模块在运行时是动态 import 的，PyInstaller 静态分析发现不了，
# 在这里显式 import 一次，确保被打包进去。
try:
    import glossary          # noqa: F401
    import zh_short          # noqa: F401
    import zh_mid1           # noqa: F401
    import zh_mid2           # noqa: F401
    import zh_batch3         # noqa: F401
    import zh_batch4         # noqa: F401
    import zh_batch5         # noqa: F401
    import zh_batch6         # noqa: F401
    import zh_batch7         # noqa: F401
    import zh_batch8         # noqa: F401
    import stage1_zh         # noqa: F401
    import zh_extra          # noqa: F401
    import tags_zh           # noqa: F401
except ImportError as _e:
    print('[警告] 部分词表模块未能加载: %s' % _e)

# config.py 与词表模块都在同一目录，可直接导入
import config


def is_admin():
    """当前进程是否具有管理员权限。"""
    try:
        import ctypes
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def relaunch_as_admin():
    """以管理员身份重新启动自己。成功返回 True。"""
    import ctypes
    if getattr(sys, 'frozen', False):
        exe = sys.executable
        params = ' '.join('"%s"' % a for a in sys.argv[1:])
    else:
        exe = sys.executable
        params = '"%s"' % os.path.abspath(__file__)
        if sys.argv[1:]:
            params += ' ' + ' '.join('"%s"' % a for a in sys.argv[1:])

    try:
        # ShellExecuteW 返回 > 32 表示成功
        r = ctypes.windll.shell32.ShellExecuteW(
            None, 'runas', exe, params, os.getcwd(), 1)
        return r > 32
    except Exception:
        return False


def can_write_resource():
    """测试是否有权限写入资源目录。"""
    if not config.RESOURCE_CN:
        return False
    try:
        os.makedirs(config.RESOURCE_CN, exist_ok=True)
        probe = os.path.join(config.RESOURCE_CN, '_wtest.tmp')
        with open(probe, 'wb') as f:
            f.write(b'x')
        os.remove(probe)
        return True
    except (OSError, PermissionError):
        return False


def ask(prompt, default='n'):
    """简单的是/否询问。"""
    suffix = ' [Y/n] ' if default == 'y' else ' [y/N] '
    try:
        ans = input(prompt + suffix).strip().lower()
    except (EOFError, KeyboardInterrupt):
        print()
        return False
    if not ans:
        return default == 'y'
    return ans in ('y', 'yes', '是', '好')


def pause():
    try:
        input('\n按回车键退出...')
    except (EOFError, KeyboardInterrupt):
        pass


BANNER = '''
================================================================
  CLIP STUDIO MODELER 简体中文汉化
================================================================
'''


def load_dictionaries():
    """合并全部词表。"""
    merged = {}

    # 官方译文
    import json
    official_path = os.path.join(BASE, 'data', 'official_dict.json')
    if os.path.exists(official_path):
        try:
            with open(official_path, encoding='utf-8') as f:
                official = json.load(f).get('en2tc', {})
            merged.update(official)
            print('  官方译文        %5d 条' % len(official))
        except Exception as e:
            print('  [警告] 官方译文读取失败: %s' % e)

    modules = [
        ('glossary', 'TERMS', '术语表'),
        ('zh_short', 'ZH', None),
        ('zh_mid1', 'ZH_MID_1', None),
        ('zh_mid2', 'ZH_MID_2', None),
        ('zh_batch3', 'ZH_BATCH3', None),
        ('zh_batch4', 'ZH_BATCH4', None),
        ('zh_batch5', 'ZH_BATCH5', None),
        ('zh_batch6', 'ZH_BATCH6', None),
        ('zh_batch7', 'ZH_BATCH7', None),
        ('zh_batch8', 'ZH_BATCH8', None),
        ('stage1_zh', 'STAGE1_ZH', None),
        ('zh_extra', 'ZH_EXTRA', None),
    ]
    for mod_name, var_name, label in modules:
        try:
            mod = importlib.import_module(mod_name)
            table = getattr(mod, var_name)
            merged.update(table)
            print('  %-14s %5d 条' % ((label or mod_name + '.py'), len(table)))
        except (ImportError, AttributeError) as e:
            print('  [跳过] %s: %s' % (mod_name, e))

    return merged


def translatable(t):
    if not t or len(t.strip()) < 2:
        return False
    if not any(c.isascii() and c.isalpha() for c in t):
        return False
    bad = ('://', '\\', 'GL_', 'gl_', '#version', 'uniform ', 'varying ',
           'void main', 'vec2 ', 'vec3 ', 'vec4 ', 'float4 ', 'sampler2D')
    if any(b in t for b in bad):
        return False
    return len(t) <= 800


def apply_resources(dictionary):
    """生成 chinese_tc 目录。"""
    replaced = 0
    total = 0
    failed = []

    if not os.path.isdir(config.RESOURCE_CN):
        os.makedirs(config.RESOURCE_CN, exist_ok=True)

    names = [n for n in sorted(os.listdir(config.RESOURCE_EN))
             if os.path.isfile(os.path.join(config.RESOURCE_EN, n))]
    print()
    print('  共 %d 个资源文件' % len(names))

    for i, name in enumerate(names, 1):
        src = os.path.join(config.RESOURCE_EN, name)
        with open(src, 'rb') as f:
            raw = f.read()

        try:
            root = parse_tree(raw, 0, len(raw))
            leaves = collect_leaves(root, [])
        except Exception as e:
            failed.append((name, str(e)))
            continue

        total += sum(1 for lf in leaves if lf.text and translatable(lf.text))

        mapping = {}
        for k, lf in enumerate(leaves):
            if not lf.text:
                continue
            zh = dictionary.get(lf.text)
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
                failed.append((name, '校验失败 %d 条' % len(bad)))
                continue

        dst = os.path.join(config.RESOURCE_CN, name)
        try:
            with open(dst, 'wb') as f:
                f.write(out)
        except PermissionError:
            print()
            print('  写入被拒绝：%s' % dst)
            print('  请确认 MODELER 已完全退出，或以管理员身份运行。')
            return None, None, failed

        replaced += len(mapping)

        if i % 8 == 0:
            print('    已处理 %d/%d ...' % (i, len(names)))

    return replaced, total, failed


def apply_tags():
    """汉化材质标签（数据库 + info.xml）。"""
    import sqlite3
    from tags_zh import TAG_ZH, SYSTEMTAG_ZH, FOLDERTAG_ZH

    if not config.USERDATA:
        print('  未找到 CELSYS 用户数据目录，跳过。')
        return

    # 数据库
    if config.CMDB and os.path.exists(config.CMDB):
        try:
            c = sqlite3.connect(config.CMDB)
            cur = c.cursor()
            n = 0
            for table, mapping in (('Tag', TAG_ZH), ('SystemTag', SYSTEMTAG_ZH),
                                   ('FolderTag', FOLDERTAG_ZH)):
                try:
                    cur.execute('SELECT _PW_ID, Title FROM "%s"' % table)
                    rows = cur.fetchall()
                except sqlite3.Error:
                    continue
                for rid, title in rows:
                    if title in mapping:
                        cur.execute('UPDATE "%s" SET Title=? WHERE _PW_ID=?'
                                    % table, (mapping[title], rid))
                        n += 1
            c.commit()
            c.close()
            print('  数据库标签    %d 行' % n)
        except sqlite3.Error as e:
            print('  数据库处理失败: %s' % e)
    else:
        print('  未找到材质数据库，跳过。')

    # info.xml
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
        for en, zh in TAG_ZH.items():
            token = '<data>%s</data>' % en
            if token in raw:
                raw = raw.replace(token, '<data>%s</data>' % zh)
                hit = True
                n_tag += 1
        if hit:
            n_file += 1
            try:
                with open(path, 'w', encoding='utf-8', newline='') as f:
                    f.write(raw)
            except OSError:
                pass
    print('  素材 info.xml %d 个文件 / %d 处' % (n_file, n_tag))


def check_language():
    """检查并提示语言标识。"""
    cfg = os.path.join(os.environ.get('ProgramData', r'C:\ProgramData'),
                       'CELSYS', 'CLIPStudio', 'InstallPath', 'modeler15.txt')
    if not os.path.exists(cfg):
        print('  未找到 modeler15.txt，若程序能显示中文可忽略。')
        return True

    try:
        with open(cfg, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
    except OSError:
        print('  无法读取 %s' % cfg)
        return False

    if 'chinese_tc' in text:
        print('  语言标识已是 chinese_tc')
        return True

    print()
    print('  语言标识当前不是 chinese_tc，需要修改才生效。')
    print('  文件：%s' % cfg)
    print()
    print('  请用【管理员权限的记事本】打开上述文件，')
    print('  把 "Language"="english" 改成 "Language"="chinese_tc"，保存后再继续。')
    print()
    pause()
    return True


def main():
    print(BANNER)

    print('提示：请先完全退出 CLIP STUDIO MODELER（含托盘图标）。')
    print()
    if not ask('准备好了吗', 'y'):
        print('已取消。')
        pause()
        return

    # 1. 路径
    print()
    print('[1/4] 检查安装位置')
    print()
    if not config.MODELER_DIR:
        print('  找不到 CLIP STUDIO MODELER 安装目录。')
        print()
        print('  请设置环境变量 MODELER_DIR 后重新运行，例如：')
        print(r'    set MODELER_DIR=D:\Program Files\CELSYS\CLIP STUDIO 1.5\CLIP STUDIO MODELER')
        print()
        pause()
        return
    config.describe()

    # 权限检查
    print()
    print('[权限] 检查写入权限')
    print()
    if can_write_resource():
        print('  有写入权限' + ('（管理员）' if is_admin() else ''))
    else:
        print('  当前没有写入资源目录的权限。')
        print('  需要以管理员身份运行。')
        print()
        if ask('是否自动请求管理员权限', 'y'):
            print()
            print('  正在请求提权，请在弹出的 UAC 窗口点【是】...')
            if relaunch_as_admin():
                print('  已启动新窗口，请在那里继续操作。')
                print('  本窗口即将关闭。')
                import time
                time.sleep(3)
                return
            else:
                print('  提权失败或被取消。')
                print('  请手动右键 exe，选择"以管理员身份运行"。')
                pause()
                return
        else:
            print('  请手动右键 exe，选择"以管理员身份运行"。')
            pause()
            return

    # 2. 语言标识
    print()
    print('[2/4] 检查语言标识')
    print()
    check_language()

    # 3. 词表
    print()
    print('[3/4] 加载词表')
    print()
    dictionary = load_dictionaries()
    print('  %-14s %5d 条（合并后）' % ('合计', len(dictionary)))

    # 4. 生成
    print()
    print('[4/4] 生成中文资源')
    if not ask('现在开始汉化'):
        print('已取消。')
        pause()
        return

    replaced, total, failed = apply_resources(dictionary)

    if replaced is None:
        pause()
        return

    print()
    print('  --------------------------------------------------')
    print('  总叶子数  : %d' % total)
    print('  已替换    : %d' % replaced)
    if total:
        print('  覆盖率    : %.1f%%' % (100.0 * replaced / total))
    print('  --------------------------------------------------')

    if failed:
        print()
        print('  有 %d 个文件处理失败：' % len(failed))
        for n, r in failed[:5]:
            print('    %s  %s' % (n[:8], r))

    # 材质标签
    print()
    if ask('是否同时汉化材质标签'):
        print()
        apply_tags()

    print()
    print('=' * 56)
    print('  完成！')
    print()
    print('  请启动 CLIP STUDIO MODELER 查看效果。')
    print('  若界面仍是英文，请检查语言标识是否为 chinese_tc。')
    print('=' * 56)
    pause()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n\n已中断。')
    except Exception as e:
        print('\n\n发生错误：%s' % e)
        import traceback
        traceback.print_exc()
        pause()
