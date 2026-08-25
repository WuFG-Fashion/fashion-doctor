---
type: concept
title: 品牌配置管理
aliases: [brand_config]
tags: [dashboard, architecture, brand, config]
sources: []
created: 2026-06-05
updated: 2026-08-26
cross_refs: []
---

# 品牌配置管理

> **分类**: L2_07 服装多品牌数据分析系统构建 > L3_07_02 品牌配置管理
> **状态**: 🔄 持续迭代中

---

## 1. 品牌配置核心结构

```python
# brand_config.py 标准模板
from typing import Dict, List, Any

BRAND_CONFIGS: Dict[str, Dict[str, Any]] = {}

def register_brand(brand_id: str, config: Dict[str, Any]):
    """注册一个品牌配置"""
    BRAND_CONFIGS[brand_id] = config

def get_brand(brand_id: str) -> Dict[str, Any]:
    """获取指定品牌配置"""
    return BRAND_CONFIGS.get(brand_id)

def get_all_brands() -> List[str]:
    """获取所有已注册品牌ID"""
    return list(BRAND_CONFIGS.keys())
```

---

## 2. 配置项详解

### 必填项
| 配置键 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| name | str | 品牌中文显示名 | "卡宾" |
| db_path | str | 数据库绝对路径 | "C:/.../cabbeen.db" |
| categories | List[str] | 一级品类 | ["上装","下装","配饰"] |
| theme_color | str | 主题色HEX | "#000000" |

### 可选项
| 配置键 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| sub_categories | dict | {} | 二级品类映射 |
| colors | list | [] | 颜色选项 |
| sizes | list | [] | 尺码选项 |
| regions | list | [] | 区域列表 |
| price_range | tuple | (0, 99999) | 价格区间 |
| logo_url | str | "" | 品牌Logo URL |

---

## 3. 品牌类型（Type）设计

系统中每个品牌可以有多个"类型"，用于进一步细分数据视图：

| 品牌ID | 类型ID | 类型名称 | 说明 |
|--------|--------|----------|------|
| peacebird_men | men | 男装 | 太平鸟男装 |
| peacebird_women | women | 女装 | 太平鸟女装 |
| peacebird_kids | kids | 童装 |太平鸟童装（LV） |
| cabbeen | main | 卡宾 | 卡宾男装（单一类型） |

### 类型配置
```python
TYPE_CONFIG = {
    "peacebird": {
        "name": "太平鸟",
        "types": ["men", "women", "kids"],
        "type_labels": {"men": "男装", "women": "女装", "kids": "童装(LV)"}
    },
    "cabbeen": {
        "name": "卡宾",
        "types": ["main"],
        "type_labels": {"main": "卡宾"}
    }
}
```

---

## 4. Tab层级设计

```
一级Tab（品牌）           二级Tab（类型/品类）     三级Tab（子品类）
┌─────────────┐
│ 太平鸟 ▼    │ →  男装 | 女装 | 童装  →  上装 | 下装 | 配饰
│ 卡宾 ▼      │ →  卡宾               →  上装 | 下装 | 配饰
│ [新增品牌]  │
└─────────────┘
```

### 实现伪代码
```python
# app.py 中的Tab构建逻辑
selected_brand = st.tabs(list(BRAND_CONFIGS.keys()))
brand_cfg = BRAND_CONFIGS[selected_brand]

if len(brand_cfg['types']) > 1:
    selected_type = st.tabs(brand_cfg['type_labels'].values())
else:
    selected_type = brand_cfg['types'][0]

selected_category = st.tabs(brand_cfg['categories'])

# 根据三层选择渲染内容
render_content(selected_brand, selected_type, selected_category)
```

---

## 5. 配置校验规则

| 规则 | 校验逻辑 | 不通过处理 |
|------|----------|------------|
| db_path存在 | os.path.exists(path) | 报错并跳过该品牌 |
| categories非空 | len(categories)>0 | 使用默认品类 |
| theme_color合法 | 匹配 ^#[0-9a-fA-F]{6}$ | 使用默认蓝色 |
| types非空 | len(types)>0 | 默认["main"] |

---

## 6. 配置热更新（可选）

```python
# 支持运行时不重启地修改配置
import json
import os

CONFIG_FILE = "config/brands.json"

def reload_configs():
    """从JSON重新加载所有品牌配置"""
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for brand_id, cfg in data.items():
        register_brand(brand_id, cfg)
```

## 关联知识

- [[system_architecture]]
- [[cross_brand_integration]]
- [[competitor_overview]]
