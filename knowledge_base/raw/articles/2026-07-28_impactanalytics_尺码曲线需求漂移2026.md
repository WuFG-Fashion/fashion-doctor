# $5B at Risk：零售尺码曲线正在漂移（Impact Analytics，2026）

> 来源：impactanalytics.ai/blog/apparel-size-shift-analysis-2026（Impact Analytics，2026）
> 主题：尺码需求结构性漂移、GLP-1 影响、store vs digital 渠道差异、缺货扭曲曲线

## 核心数据

- 超过 **4 亿件** 服装单位面临错配风险，库存价值与毛利敞口超 **$5B（50 亿美元）** 若继续按历史尺码假设规划。
- 大盘尺码占比每下降 **1 个百分点** ≈ **1.2 亿件/年** 移位；Medium 占比降 **0.75pp** ≈ **9000 万件/年** 移位。
- 单一 subclass 内 size 与 attribute 独立建模时 misallocation 可超 **5pp**。

## 关键发现

### GLP-1 驱动尺码需求漂移
- 尺码分布向小码带移动（大码未崩但稳定失份额），多数规划系统无法提前捕捉。
- 历史 size curve 基于"卖了的"非"客户想要的"——高需求尺码早期售罄，未满足需求从数据消失，曲线被静默扭曲。
- 仅看全国均值会掩盖局部（GLP-1 渗透领先市场 Medium 已软化）。

### 渠道差异（store vs digital）
- 实体店比数字渠道**更快**向小码带迁移，多数系统仍跨渠道聚合，门店级漂移被稀释。
- 买家看全公司销售数据，无法看见哪些店哪些尺码何时售罄。

### 多维度漂移
- color/fit/silhouette/finish 各维度在尺码带内独立漂移（XS/S 集中，relaxed 也缓慢同移）。

## 关键洞察

- 尺码曲线从"按 bought% 配置"转向"按 sold% 重建"是 [[sku_fine_management|服装SKU精细化管理]] 的底层数据修正。
- 与 retailnorthstar"size curve 基于 sold%"结论一致，互为印证；缺货导致的曲线失真要求 [[动态OTB管理]] 引入尺寸级售罄监控。
