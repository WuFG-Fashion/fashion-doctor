---
type: practice
title: 品牌配置驱动多品牌系统
tags: [brand, configuration, python, streamlit, multi_brand, architecture]
sources: [L3_07_02_品牌配置管理, L3_07_03_跨品牌数据整合]
created: 2026-06-08
updated: 2026-06-08
cross_refs: [[multi_brand_unified_analytics]], [[streamlit_production_dashboard]], 跨品牌数据整合, [[data_quality_governance]]
---

# 品牌配置驱动多品牌系统

> **一句话摘要**：基于Python Dict配置驱动的多品牌数据分析系统实践——通过品牌注册/品类映射/字段映射三层抽象，实现"一次开发、多品牌复用"，新增品牌仅需配置无需改代码。

> **来源**：Fashion Doctor项目实践 + L3_07_02品牌配置管理

## 一、品牌配置核心结构

```python
from typing import Dict, List, Any

BRAND_CONFIGS: Dict[str, Dict[str, Any]] = {}

def register_brand(brand_id: str, config: Dict[str, Any]):
    """注册品牌配置"""
    BRAND_CONFIGS[brand_id] = config

def get_brand(brand_id: str) -> Dict[str, Any]:
    """获取品牌配置"""
    return BRAND_CONFIGS.get(brand_id)
```

## 二、配置项设计

### 必填项
| 配置键 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| name | str | 品牌中文名 | "卡宾" |
| db_path | str | 数据库路径 | "data/cabbeen.db" |
| categories | List[str] | 一级品类 | ["上装","下装","配饰"] |
| theme_color | str | 主题色 | "#000000" |

### 可选项
| 配置键 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| sub_categories | dict | {} | 二级品类映射 |
| sizes | list | [] | 尺码选项 |
| regions | list | [] | 区域列表 |
| price_range | tuple | (0,99999) | 价格区间 |
| types | list | ["main"] | 品牌子类型 |

## 三、多品牌类型设计

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

## 四、三级Tab架构

```
一级Tab（品牌）      二级Tab（类型）    三级Tab（品类）
┌─────────────┐
│ 太平鸟 ▼    │ →  男装|女装|童装  →  上装|下装|配饰
│ 卡宾 ▼      │ →  卡宾            →  上装|下装|配饰
└─────────────┘
```

```python
# Streamlit Tab构建
selected_brand = st.selectbox("品牌", list(BRAND_CONFIGS.keys()))
brand_cfg = BRAND_CONFIGS[selected_brand]

if len(brand_cfg.get('types', [])) > 1:
    selected_type = st.selectbox("类型", brand_cfg['type_labels'].values())
else:
    selected_type = brand_cfg['types'][0]

selected_category = st.selectbox("品类", brand_cfg['categories'])

# 根据三层选择渲染
render_dashboard(selected_brand, selected_type, selected_category)
```

## 五、统一品类映射

```python
CATEGORY_MAP = {
    "outerwear": {
        "cabbeen": ["夹克","风衣","大衣","羽绒服"],
        "peacebird_men": ["外套","棉服","羽绒"],
        "gxg": ["外套"]
    },
    "tops": {
        "cabbeen": ["T恤","Polo衫","衬衫","卫衣","毛衣"],
        "peacebird_men": ["T恤","衬衫","卫衣"],
        "gxg": ["上衣"]
    },
    "bottoms": {
        "cabbeen": ["休闲裤","牛仔裤","西裤"],
        "peacebird_men": ["裤装"],
        "gxg": ["裤子"]
    }
}

def map_category(brand: str, raw_cat: str) -> str:
    """将品牌原始品类映射到统一类目"""
    for unified, mapping in CATEGORY_MAP.items():
        if raw_cat in mapping.get(brand, []):
            return unified
    return "other"
```

## 六、跨品牌对比规则

| 可直接对比 | 需谨慎对比 |
|-----------|-----------|
| 售罄率/周转天数/未动销率 | 绝对销售额（规模不同） |
| 同比/环比增长率 | 客单价（定位不同） |
| 品类占比/渠道占比 | SKU数量（策略不同） |

## 七、配置校验

```python
def validate_config(brand_id: str, cfg: dict) -> List[str]:
    """校验品牌配置有效性"""
    errors = []
    if not os.path.exists(cfg.get('db_path', '')):
        errors.append(f"{brand_id}: db_path不存在")
    if not cfg.get('categories'):
        errors.append(f"{brand_id}: categories为空")
    if not cfg.get('types'):
        cfg['types'] = ['main']  # 默认值
    return errors
```

## 八、配置热更新

```python
import json

def reload_configs(config_file: str = "config/brands.json"):
    """运行时重新加载配置，无需重启"""
    with open(config_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for brand_id, cfg in data.items():
        register_brand(brand_id, cfg)
```

## 关联知识

- [[multi_brand_unified_analytics|多品牌统一分析架构]]
- [[streamlit_production_dashboard|Streamlit生产级看板]]
- [[data_quality_governance|数据质量常态化治理]]
- [[ETL架构选型]]
- [[data_lakehouse_2026|湖仓一体2026架构]]
