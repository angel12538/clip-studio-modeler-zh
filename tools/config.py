# -*- coding: utf-8 -*-
"""路径配置：自动定位 CLIP STUDIO MODELER 安装位置。

查找顺序：
  1. 环境变量 MODELER_DIR
  2. CELSYS 的安装记录 modeler15.txt
  3. 常见默认路径

若自动定位失败，设置环境变量后重试：

  Windows 命令行：
      set MODELER_DIR=D:\\Program Files\\CELSYS\\CLIP STUDIO 1.5\\CLIP STUDIO MODELER

  PowerShell：
      $env:MODELER_DIR = 'D:\\Program Files\\CELSYS\\CLIP STUDIO 1.5\\CLIP STUDIO MODELER'
"""
import os
import re
import sys

# CELSYS 记录安装路径的文件（Windows）
INSTALL_RECORD = os.path.join(
    os.environ.get('ProgramData', r'C:\ProgramData'),
    'CELSYS', 'CLIPStudio', 'InstallPath', 'modeler15.txt')

DEFAULT_CANDIDATES = [
    r'D:\Program Files\CELSYS\CLIP STUDIO 1.5\CLIP STUDIO MODELER',
    r'C:\Program Files\CELSYS\CLIP STUDIO 1.5\CLIP STUDIO MODELER',
    r'C:\Program Files (x86)\CELSYS\CLIP STUDIO 1.5\CLIP STUDIO MODELER',
    '/Applications/CLIP STUDIO 1.5/CLIP STUDIO MODELER.app/Contents/MacOS',
]


def _from_install_record():
    """从 CELSYS 安装记录里读出 AppPath15。"""
    if not os.path.exists(INSTALL_RECORD):
        return None
    try:
        with open(INSTALL_RECORD, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
    except OSError:
        return None
    m = re.search(r'"AppPath15"\s*=\s*"([^"]+)"', text)
    if not m:
        return None
    return os.path.dirname(m.group(1))


def find_modeler_dir():
    """返回 MODELER 安装目录，找不到返回 None。"""
    env = os.environ.get('MODELER_DIR')
    if env and os.path.isdir(env):
        return env
    rec = _from_install_record()
    if rec and os.path.isdir(rec):
        return rec
    for p in DEFAULT_CANDIDATES:
        if os.path.isdir(p):
            return p
    return None


MODELER_DIR = find_modeler_dir()

if MODELER_DIR:
    RESOURCE_DIR = os.path.join(MODELER_DIR, 'resource')
    RESOURCE_EN = os.path.join(RESOURCE_DIR, 'english')
    RESOURCE_CN = os.path.join(RESOURCE_DIR, 'chinese_tc')
else:
    RESOURCE_DIR = RESOURCE_EN = RESOURCE_CN = None


def _user_data_dir():
    """CELSYS 用户数据目录（材质数据库与素材标签在这里）。"""
    if sys.platform == 'win32':
        base = os.environ.get('APPDATA', '')
        cand = os.path.join(base, 'CELSYSUserData', 'CELSYS', 'CLIPStudioCommon')
        return cand if os.path.isdir(cand) else None
    if sys.platform == 'darwin':
        return os.path.expanduser(
            '~/Library/Application Support/CELSYSUserData/CELSYS/CLIPStudioCommon')
    return None


USERDATA = _user_data_dir()
CMDB = (os.path.join(USERDATA, 'MaterialDB', 'CatalogMaterial.cmdb')
        if USERDATA else None)
MATERIAL_ROOT = os.path.join(USERDATA, 'Material') if USERDATA else None


def require_modeler():
    """确认能找到 MODELER 安装目录，否则给出清晰提示并退出。"""
    if not MODELER_DIR:
        print('错误：找不到 CLIP STUDIO MODELER 安装目录。', file=sys.stderr)
        print('', file=sys.stderr)
        print('请设置环境变量 MODELER_DIR 指向安装目录：', file=sys.stderr)
        print('  命令行: set MODELER_DIR=<安装目录>', file=sys.stderr)
        print('  PowerShell: $env:MODELER_DIR = "<安装目录>"', file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(RESOURCE_EN):
        print('错误：%s 不存在。' % RESOURCE_EN, file=sys.stderr)
        print('请确认 MODELER_DIR 指向正确，且该版本包含 resource\\english 目录。',
              file=sys.stderr)
        sys.exit(1)
    return MODELER_DIR


def describe():
    """打印当前探测结果，供诊断用。"""
    print('CLIP STUDIO MODELER 路径配置')
    print('-' * 50)
    print('安装目录  :', MODELER_DIR or '(未找到)')
    print('英文资源  :', RESOURCE_EN or '(未找到)')
    print('中文资源  :', RESOURCE_CN or '(未找到)')
    print('用户数据  :', USERDATA or '(未找到，材质标签汉化将跳过)')
    print('材质数据库:', CMDB or '(未找到)')


if __name__ == '__main__':
    describe()
