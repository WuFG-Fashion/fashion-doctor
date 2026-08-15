# 知识库优化 执行历史

| 日期 | 去重 | 断链修复 | 索引 | 基准数据 | 状态 |
|------|------|---------|------|---------|------|
| 2026-06-08 01:55 | 去重1篇(index.md重复行) | 修复44条断链(17种) | 9个L3条目 | 36文件扫描, updated | ✅ 成功 |
| 2026-06-10 01:55 | — | 修复18条断链(身体)+4条FM三层括号 | 9个L3条目 | 44文件扫描, updated | ✅ 成功 |
| 2026-06-11 01:55 | — | 修复11条断链(cross_refs格式错误) | 9个L3条目 | 46文件扫描, updated | ✅ 成功 |
| 2026-06-12 01:55 | — | 修复5条断链 | 9个L3条目 | 52文件扫描, updated | ✅ 成功 |
| 2026-06-15 02:15 | — | 修复3条断链(中文别名) | 9个L3条目 | 57文件扫描, updated | ✅ 成功 |
| 2026-06-21 02:33 | — | 修复7条断链 | 9个L3条目 | 59文件扫描, 新增bienlefen | ✅ 成功 |
| 2026-06-27 03:19 | — | 修复6条断链 | 9个L3条目 | 62文件扫描, 新增bienlefen FY2025 | ✅ 成功 |
| 2026-07-03 03:16 | — | 修复12条断链(5类) | 9个L3条目 | 66文件扫描, 新增bosideng+AI时尚消费+VIP训练营 | ✅ 成功 |
| 2026-07-09 03:20 | — | 0条断链(库高度健康) | 9个L3条目 | 67文件扫描(18 entities + 49 concepts) | ✅ 成功 |
| 2026-07-15 03:26 | — | 修复7条断链 | 9个L3条目 | 69文件扫描(19 entities + 49 concepts), updated | ✅ 成功 |
| 2026-07-21 03:23 | — | 修复19条断链(2类:反斜杠转义+中文别名) | 9个L3条目 | 71文件扫描(21 entities + 50 concepts), updated | ✅ 成功 |
| 2026-07-27 03:34 | - | 修复6条断链(slug->中文源文件名x2+服装SKU精细化管理x4) | 9个L3条目 | 74文件扫描, 新增baoxiniao/burberry/langzi_fashion(17竞品) | SUCCESS |

## 本轮详情 (2026-07-21)
- **断链**: ✅ 19条修复 (2类)
  - **反斜杠转义** 9处: `[[brand\\|label]]` → `[[brand|label]]` (MetaModels/方正/申万宏源 sources中 `[[inditex_zara\|]]` `[[hm\|]]` `[[anta\|]]` `[[hla\|]]` `[[semir\|]]` `[[bienlefen\|]]` `[[peacebird\|]]`)
  - **中文别名/错误文件名** 8处: `[[agentic_commerce]]`→`[[agentic_commerce_fashion_2026|agentic_commerce]]` (IBM source), `[[sell_through_rate]]`→`[[sell_through_examination_standard_2026|售罄率]]` (券商研报 source ×2), `[[KPI健康基准]]`→`[[china_apparel_industry_2026q1|KPI健康基准]]`, `[[服装SKU精细化管理]]`→`[[sku_fine_management|服装SKU精细化管理]]` (PANTEL+第七在线 sources), `[[沉睡会员唤醒策略]]`→`[[sleeping_member_reactivation|沉睡会员唤醒策略]]`, `[[2026-07-15_浙江日报_太平鸟30周年深度报道]]`→`[[2026-06-02_浙江日报_太平鸟30周年深度]]`
  - 2处误报保留: `[["x"]]` (code block), `[[polars_vs_pandas_2026#零售场景选型速查]]` (valid anchor)
- **孤岛**: ✅ 0个 (479个内容页面全部有出链)
- **矛盾**: ✅ 无数据矛盾 (60处自动检测均为同文件不同周期数值差异，跨文件entity↔benchmarks一致)
- **过期**: ✅ 0页过期
- **分类**: ✅ 无分类错误
- **织网**: 无需操作 (0孤岛, 全部页面已有双向链接)
- **索引**: 9个L3条目
- **基准**: updated→2026-07-21
- **Git**: 5467590

## 本轮详情 (2026-07-15)
- **断链**: ✅ 7条修复
  1. `[[数据质量常态化治理]]` → `[[data_quality_governance|数据质量常态化治理]]` (Pandas 3.0 source)
  2. `[[NVIDIA_2026零售AI全价值链落地]]` → `[[2026-07-03_NVIDIA_2026零售AI全价值链落地]]` (王府井 source)
  3. `[[kl_04_01 明星导购识别]]` → `[[AI导购陪练|明星导购识别]]` (北森 source)
  4. `[[售罄率考核基准2026]]` → `[[sell_through_examination_standard_2026|售罄率考核基准2026]]` (季中OTB source)
  5. `[[kl_04_03 导购培训体系]]` → `[[导购培训闭环体系]]` (思创 source)
  6. `[[沉睡会员唤醒策略]]` → `[[sleeping_member_reactivation|沉睡会员唤醒策略]]` (私域 source)
  7. `[[2026-07-08_迅销_优衣库日本2026年6月同店数据]]` → `[[2026-07-08_迅销_优衣库日本2026年6月同店|优衣库日本2026年6月同店数据]]` (self-ref)
  - 4处误报排除: [[#零售经济学三大变革]]+[[#AI试衣的消费者信任危机]] (valid anchor), [["x"]] (code block), [[polars_vs_pandas_2026#零售场景]] (valid anchor)
- **孤岛**: ✅ 0个 (431个内容页面全部有出链)
- **矛盾**: ✅ 无数据矛盾 (自动扫描的83处均为跨品牌误报，six_brands表结构化数据一致)
- **过期**: ✅ 0页过期
- **分类**: ✅ 无分类错误
- **织网**: 无需操作 (0孤岛, 全部页面已有双向链接)
- **索引**: 9个L3条目
- **基准**: updated→2026-07-15
- **Git**: 8750ea7

## 本轮详情 (2026-07-09)
- **断链**: ✅ 0条 (知识库高度健康)
- **孤岛**: ✅ 0个 (全部页面均有出链)
- **矛盾**: 7处
  1. fast_retailing H1营业利润 3869亿vs4006.66亿日元 (已知矛盾，已标注)
  2. inditex_zara 营收人民币换算 ~690亿 vs ~684亿 (汇率取整差异)
  3. inditex_zara 毛利率 61.2%(FY2026Q1) vs 57.8%(FY2024全年) — 周期不同，four_brands未更新
  4. inditex_zara 净利润人民币换算 ~108亿 vs ~110亿 (汇率取整差异)
  5. lululemon Q1营收 25亿 vs $24.72亿 (四舍五入，建议统一为精确值)
  6. hm Q1利润增速 +22.7% vs +25.7% (口径/来源差异)
  7. hla Q1综合毛利率: entity页缺失45.93%(仅存在于comparisons/six_brands)
- **过期**: ✅ 0页 (全部在90天内)
- **分类**: ✅ 无分类错误
- **织网**: 无需操作 (0孤岛)
- **索引**: 9个L3条目
- **基准**: updated→2026-07-09

## 本轮详情 (2026-07-03)
- **断链**: ✅ 12条修复 (5类)
  - `[[Megaview_Agent陪练2026]]` → `[[2026-06-08_百家号_Megaview_Agent陪练2026]]` (1处)
  - `[[dynamic_otb_management|动态OTB管理]]` → `[[动态OTB管理]]` (3处: retail_ai_adoption+AI商品决策)
  - `[[北森AI陪练2026三优势实测]]` → `[[2026-06-27_北森AI陪练2026三优势实测]]` (1处)
  - `[[售罄率考核基准2026]]` → `[[sell_through_examination_standard_2026|售罄率考核基准2026]]` (5处: sku+OTB+source)
  - `[[沉睡会员唤醒策略]]` → `[[sleeping_member_reactivation|沉睡会员唤醒策略]]` (2处: RFM+CLV)
  - 1处误报: `"x"` 在 polars_vs_pandas_2026.md 代码块中，已排除
- **孤岛**: ✅ 0个
- **矛盾**: ✅ 无数据矛盾 (3处自动检测均为跨品牌误报，手动验证确认)
- **过期**: ✅ 0页过期 (全部在90天内)
- **分类**: ✅ 无分类错误
- **织网**: 无需操作 (0孤岛)
- **索引**: 9个L3条目
- **基准**: updated→2026-07-03, 新增 bosideng(毛利率57.2%/净利14.6%) + ai_fashion_consumer_2026 + guide_training_camp

## 本轮详情 (2026-07-27)
- **断链**: 6条修复 (真实断链)
  - apparel_ai_agents_2026.md: 两个源文件名 slug 映射为真实中文源文件名 (style3d_blog_agentic_ai_fashion_standard -> 2026-07-26_Style3D_Blog_AgenticAI时尚科技行业标准; vistoya_fashion_ai_agents_cases -> 2026-07-26_Vistoya_2026时尚品牌AI_Agent实战)，并同步修正 frontmatter sources 行
  - 2个 source 文件: 服装SKU精细化管理 -> sku_fine_management (带别名，共4处)
  - 2处误报保留: polars_vs_pandas_2026.md 代码块 [["x"]]; data_library_selection_guide_2026.md 锚点链接 polars_vs_pandas_2026#零售场景选型速查 (有效锚点)
- **孤岛**: 0个 (全部内容页有出链)
- **矛盾**: 无数据矛盾 (跨文件同品牌同指标同周期 0 处)。跨文件扫描器初报3处候选均裁定为非矛盾:
  1. semir 146.26亿 = FY2024 (实体行"2024全年对照")，实体与源对 FY2025 均=150.90 -> 周期误标
  2. inditex 57.8% = FY2024 vs 61.2% = FY2026Q1 -> 周期不同 (库内既有惯例不计矛盾)
  3. peacebird 82.91 提取器伪影 (文件中无此值)，权威源均=63.34 -> 提取错误
- **过期**: 0页 (全部在90天内)
- **分类**: 0处 (type 与目录一致)
- **织网**: 无需操作 (0孤岛)
- **索引**: 9个L3条目 (kb_updater 重建 __index__/master_index.json)
- **基准**: 更新->2026-07-27。新增 baoxiniao/burberry/langzi_fashion (竞品总数17)。
  - 修复: 旧 _update_benchmarks.py 用实体文件名 stem 匹配导致重复/降级键 (fast_retailing/inditex_zara/muson_gxg/top_sports 误加，top_sports 覆盖 rich topsports)。已 git checkout 还原后用 update_benchmarks_controlled.py 受控重写 (仅时间戳+3新品牌，schema一致，无重复/无覆盖)。
- **Git**: a19feb1

## 本轮详情 (2026-08-02)
- **断链**: ✅ 0条真实断链（`[[polars_vs_pandas_2026#零售场景选型速查]]` 锚点链接按既有规则判定有效，保留）
- **孤岛**: ✅ 修复1个 — `sources/2026-07-28_impactanalytics_尺码曲线需求漂移2026.md` 原用单括号 `[x|y]` 伪链接（全库唯一异常，非 Obsidian 双链语法）；改为 `[[x|y]]` 并加3回链（sku_fine_management / 动态OTB管理 / 柔性供应链与商品企划）
- **矛盾**: 扫描器初报13处候选（entity/comparison/sources 同品牌同指标同周期跨文件），经裁定全部为原始来源层伪影：周期错配(迅销4260亿九个月 vs 5000亿全年；inditex 57.8%FY2024 vs 61.2%FY2026Q1)、币种换算(inditex 684亿RMB vs 87.5亿EUR)、分部vs整体(hla 4.5/34.47亿 vs 66.61亿)、取整(semir 3.0 vs 3.11亿)、跨品牌串味(jnby/lilanz 33.76↔40亿同篇)。维护层(entity+comparison) ✅ 无矛盾（与近3次 clean run 一致）
- **过期**: ✅ 0页过期（CUTOFF=2026-05-04）
- **分类**: ✅ 无分类错误
- **织网**: 修复1孤岛（双链+3回链），无新增孤岛
- **索引**: 9个L3条目（kb_updater 重建 master_index.json）
- **基准**: 刷新→2026-08-02；files_scanned=26实体+52概念；竞品维持17（anta/suhao_fashion 无财务字段、anzheng_fashion/安奈儿/jiumuwang 仅H1预告区间或扣非口径，不符合稳定基准门槛，故不新增）
- **Git**: a9b33f3

## 本轮详情 (2026-08-14)
- **断链**: ✅ 14条真实断链修复（非误报）
  - 6处三重括号合并 `[[A, [[B]]` → `[[A]], [[B]]`（深维智信/AI导购陪练/柔性供应链/动态OTB/全渠道会员/会员复购率）
  - 2处误名目标：fast_retailing `...2026H1半年业绩...`→去'半年'；peacebird `2026_06_19_...`→`2026-06-19_...`
  - 6处模板/元引用（Home/human/MOC_L04 无目标页）→ 转纯文本或保留有效 `[[CLAUDE.md]]`
  - 注：原检测器报35条，其中18条为 playbook 目标页（导购培训SOP/清仓决策树/季初订货节奏）误报——目标页实际存在，已修正 kb_lint_5rules.py resolver 纳入 playbooks/ 与 vault 根
- **孤岛**: ✅ 0个（全部内容页有出链）
- **矛盾**: ✅ 无实质数据矛盾。严格检测器初报12处（naive 18处）候选，经逐条裁定均为来源层伪影：跨币种(迅销JPY vs RMB/Inditex EUR/H&M SEK)、分部vs整体(慕尚20.56总vs19.27品牌)、指标误标(海澜210.62营收误归净利/森马28.7存货误归净利/太平鸟6.0研发误归营收)、周期误标(太平鸟2.91为2021峰值/9.47误提)、取整(太平鸟1.02→1.0)。维护层(entity+comparison+benchmarks)一致
- **过期**: ✅ 0页过期（CUTOFF=2026-05-16）
- **分类**: ✅ 0处错误（type 与目录一致）
- **织网**: 无需操作（0孤岛）
- **索引**: 权威 master_index.json（knowledge_base/__index__/）保持 9 个L3条目（L2_01:3, L2_02:6），未改动。注意 kb_updater.py 位于 tools/ 且 __file__.parent=tools/，会误写 tools/__index__/ 空索引，已清理该游离文件，未覆盖真实索引
- **基准**: 刷新→2026-08-14（updated + last_scan + files_scanned=27实体+56概念）；结构化基准块无新增（08-11/12/13 采集为来源层，已在实体/comparison 反映）
- **Git**: 待推送

## 本轮详情 (2026-08-14 18:27) — 品牌新增运行
- **任务**：用户指定新增 1 个品牌 **HumbleHumbleR（谦而不卑）**。
- **识别**：Web 核验为 2025 创立·宁波起源的中国新兴潮流男装品牌，"humble but not inferior（谦而不卑）"内核，中高端潮流男装+亲民价格带，首店 2025-09-05 宁波鄞州万达，正全国扩张。
- **操作**：
  - 新增实体 `knowledge_base/wiki/entities/humble_humble_r.md`（RAG 就绪：aliases/结论/信息链齐全，双链至 peacebird/cabbeen/男装品牌竞争格局2026Q1/服装行业竞争格局 等既有页 → 0 孤岛）。
  - `index.md` 实体表新增 1 行（⭐ NEW，含 focus 标签）。
  - `kb_benchmarks.json` `focus_brands` 35→36（纳入 humble_humble_r）。
- **lint 复核**：0 新增断链（本次链接目标均存在）；18 条断链为 concepts/playbooks/sources 既有 slug 误引（vip_tier/top_guide/selling_ability/源文件名映射等），非本次引入，留待专项修复。矛盾 18 处均为来源层伪影（维护层一致）。
- **Git**：commit 15d05d3，已推送 origin/main（33a2776..15d05d3）。仅提交 3 个目标文件，未纳入自动化临时脚本/草稿。
