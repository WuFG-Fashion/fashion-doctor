# 长期记忆（2026-04-27 更新）

## 知识库系统（L2/L3 分级 + 模块检索）

### 核心文件
- 检索模块：`C:\Users\MacBookPro\Fashion Doctor\knowledge_base\retrieval_mod.py`
- 主索引：`C:\Users\MacBookPro\Fashion Doctor\knowledge_base\__index__\master_index.json`
- CLI 入口：`C:\Users\MacBookPro\Fashion Doctor\knowledge_base\knowledge_base.py`

### 索引结构
- `L2_categories`（数组）：每个元素含 `id/name/desc/L3[]`
- L3 条目含 `id/name/path/file_count/status`
- 当前 6 条：零售基础 1 条 + 竞品分析 5 条

### CLI 用法
```
python knowledge_base.py <查询词> [--type md|pdf|excel|image|ppt|link] [--top-k N]
python knowledge_base.py --stat
python knowledge_base.py --list
python knowledge_base.py --interactive
```

### 检索防幻觉机制
- 所有摘录带来源路径 + 行号/版本
- 表格原样提取，不做计算
- 无法确认的内容标记 unverified
- 始终输出置信度（high/medium/low/unverified）

### 依赖
- requests + beautifulsoup4（链接提取器需要）
- KB 根目录：`C:\Users\MacBookPro\Fashion Doctor\knowledge_base`

---

# 2026-04-23 新增经验

## 明星导购推销能力验证关键发现

### 用户假设 vs 实际发现

| 用户假设 | 验证结果 |
|---------|---------|
| TOP3更会推TOP10款 | ⚠️ 无显著规律，10次验证中7次无差异 |
| TOP3推销能力全面领先 | ⚠️ 时间维度不同结论相反 |
| 高价值占比领先 | ✅ 60%时间段TOP3领先 |

### 10个时间段核心数据

| 时间段 | 含TOP10订单GMV | 高价值占比 |
|--------|---------------|-----------|
| 45-90天 | TOP3领先10-13pp | TOP3领先约7pp |
| 全年 | 非TOP3领先约10pp | TOP3领先约15pp |

### 关键认知

**1. 时间维度决定结论**
- 短周期（45-90天）：TOP3领先
- 长周期（全年）：非TOP3反而领先
- 不同维度结论可能完全相反

**2. 真正稳定的区分指标是高价值占比**
- 60%时间段TOP3领先
- 全年差距+15.5pp

**3. TOP3是动态的**
- 近7天TOP3：龚瑶/吕红/李志婕
- 全年TOP3：李志婕/龚瑶/潘群芳
- 需标注"当期TOP3"

**4. 推荐45天作为主要分析维度**
- 兼顾样本量和时效性

---

# 长期记忆

## Fashion Doctor 身份（2026-04-21 更新）

- **名字：** Fashion Doctor
- **根目录：** `C:/Users/MacBookPro/Fashion Doctor/`
- **原名：** 教练（零售知识库项目）
- **定位：** 服装零售数据分析独立 Agent
- **数据库：** `C:/Users/MacBookPro/cabbeen_data/cabbeen.db`

## cabbeen_data 项目关键经验

### 数据库踩坑记录（持续更新）

| 日期 | 问题 | 原因 | 解决 |
|------|------|------|------|
| 2026-04-21 | `sales.shop_name` JOIN shops 失败 | sales.shop_name 存的是**简称**（短名），不是 full_name | JOIN 用 `sales.shop_name = shops.short_name` |
| 2026-04-21 | Python 变量名含中文逗号 `disc，折` 语法错误 | 中文全角逗号不是合法字符 | 变量名只允许英文、数字、下划线 |
| 2026-04-21 | PowerShell 执行含中文 Python 脚本崩溃 | 默认 GBK 编码无法处理中文字符输出 | 前置 `$env:PYTHONIOENCODING="utf-8"` |

### 数据结构关键事实

- **sales.shop_name = shops.short_name**（已确认，2026-04-21）
- shops 表只有 5 家店，赤壁时代专卖店在 2026 年无销售
- 4家活跃店铺：赤壁摩尔城、咸宁中商、孝感吾悦、蕲春大中华
- 2026年数据日期：2026-01-01 ~ 2026-04-20
- 会员覆盖率：2026年 71.3% / 2025年 50.5%
- 折扣率口径：discount_rate 在数据库中存的是 0.x 格式（非百分比）

## 零售知识库项目

- **知识库路径：** `retail_knowledge_base.md`
- **分析脚本：** `retail_analysis_v3.py`
- **分析报告：** `retail_analysis_report.md`
- **红线规范已写入知识库顶部**：三验规则（规范文件/PRAGMA/SQL）

---

## 蜂群标准（2026-04-26 确立）

- **蜂群规范文件：**
  - HEARTBEAT.md：`C:\Users\MacBookPro\WorkBuddy\01-图灵\.workbuddy\HEARTBEAT.md`
  - reply_template.md：`C:\Users\MacBookPro\WorkBuddy\01-图灵\.workbuddy\reply_template.md`
  - shared_knowledge.md：`C:\Users\MacBookPro\WorkBuddy\01-图灵\.workbuddy\shared_knowledge.md`
- **回复规范**：所有 reply_*.md 必须按 reply_template.md 格式输出，含 JSON 状态码
- **心跳规范**：每日 09:00 前在 `.workbuddy/heartbeat/YYYY-MM-DD.md` 写入当日状态

---

## SQL 字段红线（shared_knowledge.md，2026-04-26）

> **最高优先级，禁止凭经验猜测字段，违反则清空身份重灌**

| 字段 | 唯一合法用途 | 绝对禁止场景 |
|------|------------|-------------|
| `barcode` | `SUBSTR(barcode, -2)` 提取尺码 | 款号/款色/SKU/JOIN/过滤/分组 |
| `style_code` / `style_color` | 款号/款色/SKU/款式 | 提取尺码 |

### JOIN 规则（必须严格遵守）
- `sales.shop_name = shops.short_name`（不是 full_name）
- `inventory.shop_name = shops.short_name`
- `arrival.receiver_name = shops.short_name`

### 关键字段速查
- arrival：delivery_date（非 arrival_date），shipper_name，order_type，qty
- inventory：year（非 product_year），snapshot_date，stock_tag_amount（售罄率用）
- sales：sale_date（非 date），amount（非 revenue），tag_price/tag_amount
- shops：business_unit（非 brand），full_name，short_name（JOIN用）

### 业务规则
- 售罄率 = `tag_amount / (tag_amount + stock_tag_amount) × 100%`
- VIP判断 = `(member_id IS NOT NULL AND member_id != '')`（不用 is_vip）
- inventory 快照 = 必须加 `WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM inventory)`
- 季节排序：冬 > 秋 > 夏 > 春
