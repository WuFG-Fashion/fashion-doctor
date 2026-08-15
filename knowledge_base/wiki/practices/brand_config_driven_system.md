---
type: practice
title: 品牌配置驱动多品牌系统
aliases:
  - "brand config driven system"
tags: [brand, configuration, python, streamlit, multi_brand, architecture, membership, master_data]
sources: [L3_07_02_品牌配置管理, L3_07_03_跨品牌数据整合, 2026-08-03_丽晶Semarchy_多品牌服装集团数据中台架构, 2026-08-03_多品牌服装集团数据中台架构, 2026-08-12_阿里云_数据中台落地方法论与ETL事务管理, 2026-08-15_主动元数据与多品牌数据目录2026]
created: 2026-06-08
updated: 2026-08-15
cross_refs: [[multi_brand_unified_analytics]], [[streamlit_production_dashboard]], [[data_quality_governance]], [[ETL架构选型]], [[data_lakehouse_2026]], [[全渠道会员一体化]], [[丽晶]], [[2026-08-03_多品牌服装集团数据中台架构|多品牌服装集团数据中台架构], [[2026-08-15_主动元数据与多品牌数据目录2026]]]
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

## 九、会员跨品牌通认/隔离开关（2026-08新增）⭐

> 来源：[[2026-08-03_多品牌服装集团数据中台架构|多品牌服装集团数据中台架构]]（丽晶软件 / 搜狐 / Semarchy Chantelle 案例）

多品牌集团的核心矛盾是"隔离 vs 共享"——业务层各品牌独立、决策层集团要全局视图。会员策略应做成**品牌配置里的显式开关**，而非硬编码：

```python
MEMBERSHIP_POLICY = {
    "peacebird": {
        "cross_brand": "shared",   # 跨品牌通认
        "points": "independent",    # 积分等级独立计算
        "base_info": "shared",      # 基础信息共享（姓名/手机号/生日）
        "group_view": "aggregated"  # 集团可见脱敏统计指标
    },
    "cabbeen": {
        "cross_brand": "isolated",  # 按品牌隔离
        "points": "independent",
        "base_info": "isolated",
        "group_view": "masked"      # 集团只见脱敏统计
    }
}
```

| 策略 | 含义 | 适用 |
|------|------|------|
| **跨品牌通认** | 积分等级独立计算、基础信息共享 | 集团统一会员运营、跨品牌权益互通 |
| **按品牌隔离** | 集团只见脱敏统计指标 | 品牌定位差异大、数据合规要求高 |

## 十、RCBT 主数据映射洞察（2026-08新增）⭐

国际内衣集团 Chantelle（9 品牌、10,000+ 销售点、1,500+ 集成接口）用 **RCBT（款-色-罩杯-码）** 体系跨品牌严格管控复杂商品主数据。这与国内 **款-色-码** 三级主数据同构——印证本项目的字段映射抽象具备**跨市场通用性**：

- Chantelle 的 RCBT ≈ 国内 款-色-码 + 罩杯维度（内衣特有）
- "新增品牌只需配置不需部署" = 本项目 `BRAND_CONFIGS` Dict 配置驱动的商业化对应物
- 集团中台"标准化清洗 + 统一口径"是出看板的前置闸门，与 [[data_quality_governance|数据质量治理]] 直接衔接

```python
# 在 CATEGORY_MAP 之外，显式建模主数据维度（款-色-码 / RCBT）
MASTER_DATA_DIMS = {
    "apparel": ["style", "color", "size"],
    "lingerie": ["style", "color", "band", "cup"]  # RCBT：款-色-罩杯-码
}
```

## 关联知识

- [[multi_brand_unified_analytics|多品牌统一分析架构]]
- [[streamlit_production_dashboard|Streamlit生产级看板]]
- [[data_quality_governance|数据质量常态化治理]]
- [[ETL架构选型]]
- [[data_lakehouse_2026|湖仓一体2026架构]]
- [[全渠道会员一体化|全渠道会员一体化]] — 会员跨品牌通认/隔离策略的上位方法论
- [[丽晶]] — 本实践主要出处厂商（服装零售 ERP/全渠道解决方案商）

## 数据中台主数据治理对齐（2026-08 补强）

阿里云数据中台路线强调"主数据统一视图 + 标准字典 + 分级分类"，与本项目 [[brand_config_driven_system]] 的 RCBT 主数据映射（Chantelle 9 品牌印证）一致。落地要点：治理左移（质量/合规前置到设计阶段）、三阶段渐进（先高频高价值场景）、避免一次性大而全。

> 映射：三品牌 ETL 链路（CSV→入库）应强化幂等+回滚+补偿，参见 [[multi_brand_unified_analytics]] 的 2026-08 补强。

## 2026-08-15 更新（主动元数据扩展品牌目录）

- 多品牌系统应在「品牌注册表」之上叠加**主动元数据目录**：每个品牌数据资产自动编目、打 owner、标记敏感列（自动脱敏）、记录跨品牌血缘。Autodesk 主动治理扩到 60 业务域、Kingfisher Knowledge Hub 自助排查 小时→分钟，可作参照。
- 与 [[multi_brand_unified_analytics]] 协同：品牌配置驱动开发 + 主动元数据自动编目 = 「一次配置、自动治理」。
- 来源：[[2026-08-15_主动元数据与多品牌数据目录2026]]

## 关联页面
- [[2026-08-15_主动元数据与多品牌数据目录2026]]

- [[2026-08-06_ETL_ELT_ETLT混合架构与电商数据工程四层]]
- [[bi_dashboard_retail_deployment]]

- [[2026-08-12_阿里云_数据中台落地方法论与ETL事务管理]]
