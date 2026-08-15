# 给 _automation_A1/A2/A3.md 追加第九步（置信度 + 上下文护栏）
import os

tail_marker = "   - 若本轮无新增，明确标注「✅ 库已覆盖，仅补缺口/无重复造页」"

ninth_template = """## 第九步：置信度标注与上下文护栏（强制）

### 9.1 置信度（数据可信度分级，依据 CLAUDE.md 2.4）
- 每个新建 `wiki/sources/` 页 frontmatter 必须含 `confidence`（取值：财报 / 官方公告 / 第三方数据 / 品牌自宣 / 媒体估算），并在页内“来源链接”上方用 `> **置信度**：xxx` 显式声明。
- 更新 entity 页时，关键数字（营收 / 利润 / 门店数等）在正文内联标注，如 `营收 28.78 亿（置信度：财报）`；凡“约 / 估”数据必须标 `（置信度：媒体估算）`。
- 矛盾检测（第六步）须优先比对同 `confidence` 等级数据；跨等级冲突以高等级为准，并在页末 `⚠️ 数据矛盾` 注明等级差异。

### 9.2 上下文护栏（防单轮 12 品牌全维度检索溢出 / 尾部降级）
- **每品牌 WebSearch 上限 3 次**（含探针），超出即停止该品牌检索并记“已达检索上限”。
- **优先 WebSearch 摘要**，非必要不 WebFetch 整页；整页仅用于财报 / 公告原文核验。
- **第 6 个品牌写入完成后做一次中途 git commit**（命令见下），将前半程落盘，缩小爆炸半径、提供干净续跑点。
- 若执行至品牌 10+ 时察觉自身检索变浅 / 格式漂移，允许对剩余品牌仅做探针 + 记录“需复核”，**不得强行编造数据**。

### 9.3 分段提交（替换原第七步单次提交）
- 前半程（品牌 1-6 写完）：`git pull --ff-only || true && git add knowledge_base/ && git commit -m "[auto] Round A{n} — 前半程(品牌1-6)"`
- 后半程（品牌 7-12 写完）：`git pull --ff-only || true && git add knowledge_base/ && git commit -m "[auto] Round A{n} — 后半程(品牌7-12)" && git push`
"""

files = {
    "_automation_A1.md": "1",
    "_automation_A2.md": "2",
    "_automation_A3.md": "3",
}

for f, n in files.items():
    assert os.path.exists(f), f
    s = open(f, encoding="utf-8").read()
    assert tail_marker in s, f"tail marker not found in {f}"
    if "## 第九步" in s:
        print("skip (already has 第九步):", f)
        continue
    block = ninth_template.replace("{n}", n)
    s2 = s.rstrip() + "\n\n" + block.strip() + "\n"
    open(f, "w", encoding="utf-8").write(s2)
    print("appended 第九步:", f, "(A" + n + ")")
