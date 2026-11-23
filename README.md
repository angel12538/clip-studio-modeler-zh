# CLIP STUDIO MODELER 简体中文汉化

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)

把 CELSYS 的 **CLIP STUDIO MODELER** 国际版界面汉化为简体中文的工具集。

CELSYS 官方从未发布过 CLIP STUDIO MODELER 的中文版——[官方问答](https://ask.clip-studio.com/en-us/detail?id=120676)明确说明该软件只有英语和日语，软件本身无法切换中文。

本项目通过逆向其资源文件格式，自行构建中文资源，实现界面汉化。**不包含任何 CELSYS 版权文件**，仅提供转换工具与译文词表。

---

## 效果

| 范围 | 覆盖率 |
|---|---|
| 界面文字 | 6657 / 6906（**96.4%**） |
| 材质标签 | 10 个全部 |
| 素材标签（info.xml） | 82 个文件 / 194 处 |

已汉化的部分包括：菜单栏、面板标题、工具栏、对话框、错误提示、
材质分类树、素材标签、快捷键说明等。

剩余约 2.7% 为**不可翻译的技术项**：文件格式名（`DXF`/`3DS`/`PNG`）、
文件过滤器、颜色空间缩写（`RGB`/`CMYK`）、单位（`mm`/`pt`/`px`）、
内部标识符与 XML 模板——改动它们会破坏文件读写与格式匹配。

---

## 原理

### 关键发现

`CLIPStudioModeler.exe` 的语言清单里一直有 `chinese_sc` 和 `chinese_tc`，
只是官方安装包的 `resource\` 下从未提供这两个目录。

```
japanese · english · chinese_sc · chinese_tc · french · spanish · korean · german · other
```

程序按 `modeler15.txt` 里的语言标识去找对应的资源目录：

```ini
"AppPath15"="...\CLIPStudioModeler.exe";
"AppName"="MODELER";
"Sort"="500";
"Language"="english";        ← 改成 chinese_tc
```

所以汉化的思路是：**改语言标识 + 自建中文资源目录**，原版 `resource\english\` 完全不动。

### 资源文件格式

通过对比同一文件的四种语言版本反推得出（同一 GUID 文件，日文 602 字节、
韩文 560 字节、繁中 536 字节、英文 536 字节——长度可变）。

每个资源文件是一棵**递归分段树**：

```
节点 = [u32 子段数 N][N × {u32 id, u32 偏移, u32 长度}]
叶子 = [u32 长度][UTF-8 文本]

约束：同层子段首尾相接无空隙，且精确覆盖父段范围
```

改字符串长度的正确做法是**自底向上重建**：先排布叶子，再逐层回填偏移。

解析与重建实现在 [`tools/celsys_tree.py`](tools/celsys_tree.py)。

**验证结果：**

| 测试 | 结果 |
|---|---|
| 精确往返（不改内容重建） | 32/32 通过 |
| 改长度后重新解析结构一致 | 31/31 通过 |
| 写入 625 条中文回读校验 | 625/625 通过 |

### 译文来源

按优先级三路合并：

1. **术语表** `tools/glossary.py` —— 自定义，遵循「材质 / 资源」规范
2. **CELSYS 官方译文** —— 用日文当桥梁回收：
   ```
   MODELER 英文 → MODELER 日文 → PAINT 日文 → PAINT 繁中 → 简体
   ```
   共 3146 条，占全部工作的 46%
3. **人工翻译** —— 其余部分，按批次整理为 `tools/zh_*.py`

优先采用官方译文的原因是术语体系一致，不会出现同一功能两套叫法。

---

## 使用方法

### 环境要求

- Windows（本工具在 Windows 10/11 + Python 3.12 下测试）
- Python 3.8 或更高
- 已安装正版 CLIP STUDIO MODELER（国际版，带 `resource\english\` 目录）
- 运行 MODELER 至少一次（生成材质数据库）

### 步骤

**1. 获取本项目**

```bash
git clone https://github.com/angel12538/clip-studio-modeler-zh.git
cd clip-studio-modeler-zh
```

**2. 修改语言标识**

用**管理员权限**的记事本打开：

```
C:\ProgramData\CELSYS\CLIPStudio\InstallPath\modeler15.txt
```

把 `"Language"="english"` 改为 `"Language"="chinese_tc"`，保存。

> 该文件权限较严，普通编辑会被拒绝访问。

**3. 生成中文资源**

```bash
python tools/apply_all.py           # 预演，看看会替换多少条
python tools/apply_all.py --apply   # 实际写入
```

脚本会自动定位 MODELER 安装目录。若定位失败，手动指定：

```bat
set MODELER_DIR=D:\Program Files\CELSYS\CLIP STUDIO 1.5\CLIP STUDIO MODELER
```

**4. 汉化材质标签（可选）**

```bash
python tools/apply_tags.py --apply
```

> 执行前请完全退出 MODELER，否则内存中的旧标签会在退出时覆盖磁盘改动。

**5. 启动 MODELER**

界面即为简体中文。

### 查看进度

```bash
python tools/progress.py
```

### 还原

```bash
python tools/rollback.py --apply
```

会删除中文资源目录、用反向词典把材质标签改回英文。
语言标识需手动改回 `english`。

---

## 已知限制

**说明文字行距偏挤**

对话框里多行长说明文字会有轻微重叠。控件行高按英文字形设计，中文比英文高。
CELSYS 自己的日文版也有同样问题。已把长段落压缩到 2~3 行尽量减少影响，但无法根治。

**更新后需重做**

卸载重装或安装官方更新后：
- `modeler15.txt` 的语言标识会被重置为 `english`
- `resource\chinese_tc\` 可能被删除或失效

重新执行上面步骤 2-4 即可，词表都在。

---

## 项目结构

```
clip-studio-modeler-zh/
├── tools/
│   ├── config.py           路径自动探测
│   ├── celsys_tree.py      ★ 资源格式解析与重建
│   ├── apply_all.py        一键汉化（合并全部词表）
│   ├── apply_tags.py       材质标签汉化
│   ├── progress.py         进度统计
│   ├── rollback.py         还原
│   ├── glossary.py         术语表
│   ├── zh_short.py         短串词表
│   ├── zh_mid1.py          中串词表 1
│   ├── zh_mid2.py          中串词表 2
│   ├── zh_batch3.py ～ 8   各批次词表
│   ├── stage1_zh.py        首批界面词表
│   ├── tags_zh.py          材质标签词表
│   └── data/
│       └── official_dict.json   回收的官方译文（3146 条）
├── docs/
│   └── FORMAT.md           资源文件格式详解
├── LICENSE                 MIT
└── README.md
```

---

## 版权声明

**本项目不包含任何 CELSYS 的版权文件。**

- 不分发 `CLIPStudioModeler.exe` 或任何资源文件
- 不分发汉化后的 `resource\chinese_tc\` 目录
- 仅提供自行编写的解析/重建工具与译文词表

`resource\chinese_tc\` 由使用者在本机自行生成，所使用的原始资源来自其合法安装的软件。

`CLIP STUDIO` 与 `CLIP STUDIO MODELER` 是 CELSYS, Inc. 的商标或注册商标。
本项目与 CELSYS 无任何关联，未获其授权或认可。

使用者需自行拥有正版 CLIP STUDIO MODELER 授权。

---

## 致谢

- 资源格式反推参考了同一套引擎的其他 CELSYS 产品结构
- 官方译文回收借助了 CLIP STUDIO PAINT 的繁体中文资源

## 许可

[MIT](LICENSE)
