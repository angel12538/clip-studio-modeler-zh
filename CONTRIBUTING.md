# 贡献指南

感谢你愿意参与这份工作。

## 最有价值的贡献

### 1. 补充或修正译文

发现译文不准确、术语不统一，或者有漏译，直接改对应的词表：

| 文件 | 内容 |
|---|---|
| `tools/glossary.py` | 核心术语（优先级最高） |
| `tools/zh_short.py` | 12 字节以内的短串 |
| `tools/zh_mid1.py` / `zh_mid2.py` | 中等长度串 |
| `tools/zh_batch3.py` ~ `zh_batch8.py` | 各批次词表 |
| `tools/stage1_zh.py` | 首批界面词表 |
| `tools/zh_extra.py` | 模板与长段落 |
| `tools/tags_zh.py` | 材质标签 |

修改后跑一次验证：

```bash
python tools/apply_all.py           # 预演，确认替换条数变化合理
python tools/progress.py            # 看覆盖率
```

### 2. 术语规范

统一遵循「**材质 / 资源**」体系：

| 英文 | 采用 | 避免 |
|---|---|---|
| Material | 材质 | 素材 |
| Texture | 纹理 | 材质 |
| Asset / Resource | 资源 | 素材 |
| Object | 对象 | 物件 |

若发现某处不符合，欢迎提 PR。

### 3. 报告问题

提 Issue 时请附上：

- CLIP STUDIO MODELER 版本号
- 出问题的界面位置（截图最好）
- 英文原文与当前译文

---

## 提交前请确认

1. **不要提交 CELSYS 的版权文件**

   `backup/` 目录已在 `.gitignore` 中排除，请勿强行添加。
   包括：`resource\english\`、`resource\chinese_tc\`、`CatalogMaterial.cmdb`、任何 `info.xml`。

2. **词表格式**

   ```python
   ZH_XXX = {
       'English original': '中文译文',
   }
   ```

   - 键必须是 `resource\english\` 里的**完整原文**，包括前后空格和 `\r\n`
   - 不翻译的条目（格式名、单位、内部键）请**不要放进来**

3. **长文本要手动断行**

   对话框说明文字所在的控件不会自动折行，必须用 `\r\n` 按宽度手动分。
   控件可用宽度约 550px（中文约 10px/字，半角约 5px/字）。
   建议每行控制在 300px 以内。

---

## 代码风格

- Python 3.8+，不引入第三方依赖（`opencc` 仅用于生成官方译文，运行时可不需要）
- 文件用 UTF-8 无 BOM
- 注释用中文，说明「为什么」而不只是「做什么」

---

## 提交流程

```bash
git checkout -b fix/术语修正
# 修改词表
python tools/apply_all.py    # 预演验证
git add tools/
git commit -m "修正 Mesh 相关术语为「网格」"
git push origin fix/术语修正
```

然后在 GitHub 上提 Pull Request。

---

## 许可

提交的代码与译文默认以 [MIT](LICENSE) 协议授权。
