## v1.1.1 · 语言标识全自动 + 修复写入截断风险

### 主要变化

**语言标识不再需要手动改。**

之前 exe 只提示你去改 `modeler15.txt`，现在它会在启动时请求管理员权限，
然后自己把 `"Language"` 改成 `chinese_tc`。

`一键汉化.cmd` 同样：检测到不对就自动提权修改，改完再校验。

### 修复的严重问题

**旧实现会把配置文件写成 0 字节。**

原因：`File.WriteAllText` 和 `open(path, 'w')` 都是**先截断再写**。
一旦写入被拒绝（该文件 ACL 限制很严），目标文件就变成空的了：

```
modeler15.txt   0 字节   ← 坏掉，MODELER 无法启动
```

新版改用安全流程：

```
写临时文件 .new
  → 读回校验内容一致
  → 删除原文件
  → 移动临时文件到位
  → 最终校验 Language 值

任一步失败 → 从 .bak 自动恢复
```

实测验证：`english`(153 字节) → `chinese_tc`(159 字节)，内容完整、校验通过。

### 另一个坑

`set_language.ps1` 里原本写了中文注释，但 **powershell.exe 在中文系统上按 ANSI 读取 .ps1**，
中文注释的尾字节会吞掉后面的换行，导致 `try {` 被并进注释、语法报错。

已改为纯 ASCII（英文注释），并在文件头注明原因。

### 使用

下载 `MODELER-ZH-v1.1.1-win64.zip`，解压后双击 `MODELER-ZH.exe`：

```
1. 请求管理员权限（UAC 点「是」）
2. 自动修改语言标识
3. 生成中文资源
4. 询问是否汉化材质标签
```

全程无需手动改任何文件。

### 升级注意

如果之前跑过 v1.1.0 且 `modeler15.txt` 变成 0 字节，本版会自动从 `.bak` 恢复。

手动恢复方法：

```cmd
copy /Y "C:\ProgramData\CELSYS\CLIPStudio\InstallPath\modeler15.txt.bak" ^
        "C:\ProgramData\CELSYS\CLIPStudio\InstallPath\modeler15.txt"
```

（需管理员权限的 cmd）

---

本版同样**不包含任何 CELSYS 版权文件**。
