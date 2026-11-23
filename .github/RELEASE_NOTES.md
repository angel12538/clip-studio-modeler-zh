## CLIP STUDIO MODELER 简体中文汉化 v1.0.0

首次发布。

### 成果

| 范围 | 覆盖率 |
|---|---|
| 界面文字 | 6657 / 6906（**96.4%**） |
| 材质标签 | 10 个全部 |
| 素材标签 info.xml | 82 个文件 / 194 处 |

已汉化：菜单栏、面板标题、工具栏、对话框、错误提示、材质分类树、
素材标签、快捷键说明。

### 核心突破

`CLIPStudioModeler.exe` 的语言清单里一直有 `chinese_sc` / `chinese_tc`，
只是官方安装包从未提供对应资源目录。

逆向出资源文件格式为**递归分段树**：

```
节点 = [u32 段数 N][N × {u32 id, u32 偏移, u32 长度}]
叶子 = [u32 长度][UTF-8 文本]
约束：同层子段首尾相接、无空隙
```

改字符串长度需自底向上重建。验证结果：精确往返 32/32、
结构一致性 31/31、写入回读 625/625。

### 使用方法

```bash
# 1. 修改语言标识（需管理员权限）
#    C:\ProgramData\CELSYS\CLIPStudio\InstallPath\modeler15.txt
#    "Language"="english"  ->  "Language"="chinese_tc"

# 2. 生成中文资源
python tools/apply_all.py --apply

# 3. 汉化材质标签（可选，需先退出 MODELER）
python tools/apply_tags.py --apply
```

详见 [README](https://github.com/angel12538/clip-studio-modeler-zh#使用方法)。

### 已知限制

- **说明文字行距偏挤**：控件行高按英文字形设计，中文更高。CELSYS 日文版同样存在此问题，无法通过改字符串根治。
- **更新后需重做**：卸载重装或官方更新会把语言标识重置，重新执行步骤 1-3 即可。

### 版权说明

本发布**不包含任何 CELSYS 版权文件**。

- 不分发 `CLIPStudioModeler.exe` 或任何资源文件
- 不分发汉化后的 `resource\chinese_tc\` 目录
- 仅提供解析/重建工具与译文词表

使用者需自行拥有正版 CLIP STUDIO MODELER 授权。
`CLIP STUDIO` 是 CELSYS, Inc. 的商标，本项目与其无关联、未获授权。

### 协议

MIT
