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
    """以管理员身份重新启动自己，带上 --elevated 标记避免无限循环。"""
    import ctypes
    args = [a for a in sys.argv[1:] if a != '--elevated']
    args.append('--elevated')

    if getattr(sys, 'frozen', False):
        exe = sys.executable
        params = ' '.join('"%s"' % a for a in args)
    else:
        exe = sys.executable
        params = '"%s" ' % os.path.abspath(__file__)
        params += ' '.join('"%s"' % a for a in args)

    try:
        r = ctypes.windll.shell32.ShellExecuteW(
            None, 'runas', exe, params, os.getcwd(), 1)
        return r > 32
    except Exception:
        return False


def config_path():
    """modeler15.txt 的路径。"""
    return os.path.join(
        os.environ.get('ProgramData', r'C:\ProgramData'),
        'CELSYS', 'CLIPStudio', 'InstallPath', 'modeler15.txt')


def read_language():
    """读取当前语言标识，失败返回 None。"""
    p = config_path()
    if not os.path.exists(p):
        return None
    try:
        with open(p, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
    except OSError:
        return None
    import re
    m = re.search(r'"Language"\s*=\s*"([^"]*)"', text)
    return m.group(1) if m else None


def set_language(target='chinese_tc'):
    """把语言标识改为指定值。

    安全措施：open(path, 'w') 会先截断目标文件再写，
    一旦写入被拒就会留下 0 字节的坏文件。
    所以改为：写临时文件 -> 校验 -> 替换，失败则从备份恢复。

    返回 (成功, 说明)。
    """
    import re
    import shutil

    p = config_path()
    if not os.path.exists(p):
        return False, '找不到 %s' % p

    bak = p + '.bak'
    tmp = p + '.new'

    # 读取原内容；若已是坏的则尝试从备份恢复
    try:
        with open(p, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
    except OSError as e:
        return False, '无法读取：%s' % e

    if len(text) < 20:
        if os.path.exists(bak):
            try:
                with open(bak, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()
            except OSError:
                return False, '目标文件为空且备份不可读'
        else:
            return False, '目标文件为空且无备份'

    # 刷新备份
    try:
        with open(bak, 'w', encoding='utf-8', newline='') as f:
            f.write(text)
    except OSError:
        pass

    if '"Language"="%s"' % target in text:
        return True, '已是 %s' % target

    new = re.sub(r'"Language"\s*=\s*"[^"]*"',
                 '"Language"="%s"' % target, text)
    if new == text:
        return False, '文件里没有找到 Language 行'
    if 'AppPath15' not in new:
        return False, '替换结果异常，已中止'

    # 写临时文件并校验
    try:
        with open(tmp, 'w', encoding='utf-8', newline='') as f:
            f.write(new)
        with open(tmp, 'r', encoding='utf-8') as f:
            if f.read() != new:
                os.remove(tmp)
                return False, '临时文件校验失败'
    except PermissionError:
        return False, '没有写入权限'
    except OSError as e:
        try:
            os.remove(tmp)
        except OSError:
            pass
        return False, '写入临时文件失败：%s' % e

    # 替换
    try:
        os.remove(p)
        os.replace(tmp, p)
    except OSError as e:
        # 替换失败：从备份恢复，不留坏文件
        try:
            if os.path.exists(bak):
                shutil.copy2(bak, p)
        except OSError:
            pass
        try:
            os.remove(tmp)
        except OSError:
            pass
        return False, '替换失败（已尝试恢复备份）：%s' % e

    # 最终校验
    try:
        with open(p, 'r', encoding='utf-8', errors='ignore') as f:
            final = f.read()
    except OSError:
        return False, '无法读回最终文件'

    if '"Language"="%s"' % target in final and len(final) > 20:
        return True, '已改为 %s' % target
    return False, '最终校验未通过'


def ensure_language():
    """确保语言标识为 chinese_tc。已是则跳过，否则直接修改。"""
    cur = read_language()
    if cur is None:
        print('  未找到 modeler15.txt，跳过（若程序能显示中文可忽略）')
        return True
    if cur == 'chinese_tc':
        print('  已是 chinese_tc，无需修改')
        return True

    print('  当前为「%s」，正在改为 chinese_tc...' % cur)
    ok, msg = set_language('chinese_tc')
    if ok:
        print('  %s' % msg)
        return True

    print('  修改失败：%s' % msg)
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
    # ---------- 提权：修改语言标识与写入资源目录都需要管理员 ----------
    elevated = '--elevated' in sys.argv
    if sys.platform == 'win32' and not is_admin() and not elevated:
        print(BANNER)
        print('本工具需要管理员权限：')
        print('  · 修改语言标识 modeler15.txt')
        print('  · 写入 MODELER 安装目录的资源文件')
        print()
        print('正在请求提权，请在弹出的 UAC 窗口点【是】。')
        print('若已取消，本窗口会以普通权限继续（可能失败）。')
        print()

        if relaunch_as_admin():
            print('已在管理员窗口中启动，本窗口即将关闭...')
            import time
            time.sleep(2)
            return
        print('提权未成功，以普通权限继续。')
        print()
        try:
            input('按回车继续...')
        except (EOFError, KeyboardInterrupt):
            return
        print()

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

    # 2. 语言标识（自动修改）
    print()
    print('[2/4] 检查语言标识')
    print()
    ensure_language()

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
