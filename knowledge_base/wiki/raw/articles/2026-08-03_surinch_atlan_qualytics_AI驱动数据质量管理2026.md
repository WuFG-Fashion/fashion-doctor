# AI 驱动数据质量管理 2026：从规则驱动到智能预防

**采集日期**：2026-08-03
**来源**：
1. surinch《AI 驱动数据质量管理实战指南：从规则驱动到智能预防》https://surinch.com/resources/ai-driven-data-quality-management
2. Qualytics《Qualytics Launches Data Control Layer to Govern Context for AI Systems》2026-04-13 https://qualytics.ai/resources/in/data-control-layer-to-govern-context-for-ai-systems
3. Atlan《How to Build Data Quality Rules for AI Success in 2026》https://atlan.com/know/data-quality-rules
4. Google Cloud Codelab《Programmatic Data Quality with Dataplex and Generative AI》2026-03-28

---

## 一、2026 核心变革：被动修复 → 主动预防

传统数据质量管理依赖固定规则和阈值，存在三大问题：
- 规则维护成本高
- 漏报误报多
- 被动响应（问题发生后才发现）

2026 年的转向：**规则 + 统计 + AI 辅助结合**，从事后修复走向事中控制与事前预防。

## 二、AI 的四类候选能力（均需人工确认）

| 能力 | 说明 | 边界 |
|------|------|------|
| 智能异常检测 | 识别不符合历史分布的数据模式 | 需真实基线验证 |
| 预测性质量监测 | 预测质量下降趋势 | 需持续反馈校准 |
| 根因分析辅助 | 定位问题来源层级 | 人工确认结论 |
| 修复建议生成 | 生成清洗/修正方案 | **不能直接改生产数据** |

**上线边界（硬约束）**：AI 输出只能进入确认流程，不能直接写生产数据。关键节点必须人工审核。

## 三、实施四阶段

1. 现状评估和目标设定
2. 数据质量基线建立
3. AI 模型训练和验证
4. 生产部署和持续优化

建议从小范围试点开始，验证效果后再扩展。

## 四、ROI 四维度量化

- 问题减少率
- 发现时间缩短
- 维护成本降低
- 数据可信度提升

> 注意：**不要用供应商示例替代客户自己的基线和复盘口径**。

## 五、口径不一致的排查顺序（重要方法论）

当问题表现为"源系统、数仓与报表结果不一致"时，先冻结以下 7 项，再判断是数据缺失、转换差异还是指标定义冲突：

1. 各层截止时间
2. 时区
3. 粒度
4. 过滤条件
5. 晚到规则（late-arriving data）
6. 口径版本
7. 精度

## 六、Qualytics Data Control Layer（2026-04-13 发布）

**核心命题**：AI 系统从"回答问题"转向"执行决策"后，坏数据不再只是报表不准，而是以机器速度驱动自动化动作、财务过账和跨系统工作流。

**validate-at-use 模型**：在数据驱动决策的那一刻做校验，而非只在管道下游做静态检查。

关键数据：
- 客户平均在生产环境运行 **20,000+ 条规则**
- 其中 **95% 由 AI 推断生成**

三大能力：
1. AI 负责规模覆盖 + 人工负责治理导向的增强型质量覆盖
2. 业务团队、数据团队、AI 系统共享同一套质量定义基础
3. 实时信号作为数据使用处的控制点

接入方式：
- 内部：Qualytics 平台 UX + AgentQ 对话式界面
- 外部 copilot：ChatGPT / Claude / Microsoft Copilot 通过 **MCP（Model Context Protocol）** 访问受治理的质量信号
- 自治系统：Qualytics API 实时评估质量并强制阈值

CTO Eric Simmerman 原话："Observability tells you what happened. The data control layer governs what happens next."（可观测性告诉你发生了什么，数据控制层治理接下来会发生什么。）

## 七、Atlan：2026 数据质量规则六大最佳实践

1. **按业务价值排优先级**：识别驱动 80% 业务价值的 20% 数据元素，先在此建规则
2. **实施数据契约（Data Contracts）**：在源头强制质量规则，让数据生产者对进仓前的数据健康负责
3. **创建可复用规则模板**：邮箱校验逻辑一次定义，复用于客户邮箱/员工邮箱/供应商联系邮箱
4. **利用 AI 与主动元数据**：2026 年手工建规则无法规模化，用 AI 基于历史模式自动建议规则
5. **自动化数据管家与修复**：每条规则映射到具体 data steward，规则失败立即触发工作流
6. **透明沟通质量指标**：通过率、趋势线、违规模式对所有干系人可见

**三个核心度量**：
- **Data uptime**：关键数据资产满足全部质量规则的时间百分比（数据团队的终极 SLO）
- **TTD（Time to Detection）**：规则失败到告警发出的平均时间
- **Data quality ROI**：预防停机与人工清洗节省的成本 vs 治理工具与人力成本

**四大常见挑战**：
- 碎片化下的规模化难题（中心枢纽质量高、源头质量差）
- 缺乏业务上下文（技术团队闭门造规则）
- 规则腐化与告警疲劳（schema 演进后旧规则误报激增，团队开始忽略告警）
- 修复瓶颈（发现错误但无人认领，失败检查在队列里躺几天）

## 八、Google Dataplex + Gemini：policy-as-code 路径

Codelab 演示"code-first"治理：
- Materialized View 打平嵌套 BigQuery 数据 → 全量剖析
- Dataplex Python Client 编程触发 profile scan
- 导出 profile 数据 → 结构化为生成式模型输入
- Gemini CLI 分析 profile 并生成符合 Dataplex 规范的 YAML 规则文件
- **HITL（Human-in-the-Loop）** 交互式验证 AI 生成配置
- 部署为自动化质量扫描

核心目标：从手工 UI 驱动流程，转为可版本控制的 policy-as-code 框架，可纳入 CI/CD。

---

## 对服装零售的适配启示

- 服装零售 SKU 维度（款/色/码）字段多、跨系统（POS/ERP/电商/WMS/CRM）口径分裂严重，是"规则腐化"高发区，适合用 AI 规则推荐 + 人工确认降低维护成本
- validate-at-use 对"AI 导购/自动补货 Agent"类场景尤其关键——坏数据会直接触发错误补货单
- Data uptime / TTD 可作为多品牌数据看板自身的健康度 KPI
