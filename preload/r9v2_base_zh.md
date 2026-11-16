# R9V2 基础预加载（Chinese Translation）

> **译者注**：此文件基于 `preload/r9v2_base.md` 翻译而来，保留了所有章节编号、代码块以及关键术语。已由人工审校，确保译文准确。

## 1. 概述

本节提供了 R9V2 基础预加载的总体概览。它描述了系统在启动时需要加载的核心资源以及它们的相互关系。

## 2. 关键资源列表

| 资源编号 | 资源名称 | 描述 |
|----------|----------|------|
| 1 | 核心库 (`core-lib`) | 提供基础运行时功能的核心库。 |
| 2 | 配置文件 (`config.yaml`) | 包含系统默认配置的 YAML 文件。 |
| 3 | 本地化资源 (`i18n/zh_CN.json`) | 中文本地化字符串集合。 |

> **注意**：上述资源的编号（1、2、3）与英文原文保持一致，以便在跨语言对照时不产生歧义。

## 3. 加载顺序

1. **加载核心库**：系统首先加载 `core-lib`，确保运行时环境已准备好。
2. **读取配置文件**：随后读取 `config.yaml`，将默认配置注入运行时。
3. **应用本地化资源**：最后加载 `i18n/zh_CN.json`，为用户界面提供中文本地化支持。

## 4. 示例代码片段

```python
# 示例：初始化预加载流程
import core_lib
import yaml
import json

# 加载核心库
core_lib.initialize()

# 读取配置
with open('config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

# 加载中文本地化
with open('i18n/zh_CN.json', 'r', encoding='utf-8') as f:
    i18n = json.load(f)

print('预加载完成，系统已准备好运行。')
```

## 5. 常见问题 (FAQ)

**Q1：如果 `i18n/zh_CN.json` 缺失会怎样？**
> 系统将回退到默认的英文本地化字符串，并在日志中记录警告。

**Q2：如何自定义加载顺序？**
> 可以通过修改 `preload/loader.yaml` 中的 `order` 列表来重新排列资源加载顺序。

---

*此文件遵循项目的文档风格指南，并已通过 `prose_provenance` 生成相应的元数据。*