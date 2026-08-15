# -*- coding: utf-8 -*-
"""Batch-insert brand_specific + superseded_by into A1/A2/A3/C spec files."""
import re, pathlib

BASE = pathlib.Path(r"D:\Fashion Doctor\fashion-doctor")

# --- Pattern 1: Add to 第四步 write section ---
# Insert after the "结论+信息链" line, before "同步到 L2/L3"
WRITE_OLD_A = "- ⚠️ 每个新建/更新的 concept/entity/comparison 页必须含 `## 结论`（2-4 条合成洞察，是判断而非数据复述）与 `## 信息链`（上游来源 → 本页 → 下游实体/对比/打法 的双链推理链），遵循 CLAUDE.md 2.3/5.1\n- 同步到 L2/L3 历史目录"
WRITE_NEW_A = "- ⚠️ 每个新建/更新的 concept/entity/comparison 页必须含 `## 结论`（2-4 条合成洞察，是判断而非数据复述）与 `## 信息链`（上游来源 → 本页 → 下游实体/对比/打法 的双链推理链），遵循 CLAUDE.md 2.3/5.1\n- ⚠️ **brand_specific 标注（CLAUDE.md 2.5）**：每个新 source 页 frontmatter 必须含 `brand_specific: true/false`——品牌特有数据标 `true`（双链到品牌实体页），行业通用方法论标 `false`（双链到 concept，不链品牌）\n- ⚠️ **superseded_by 回填（CLAUDE.md 2.5）**：写入新 source 时，检查是否有同品牌同指标的旧 source，有则在旧 source frontmatter 回填 `superseded_by: \"[[新source]]\"`\n- 同步到 L2/L3 历史目录"

WRITE_OLD_C = "- ⚠️ 每个新建/更新的 concept/practice 页必须含 `## 结论`（2-4 条合成洞察，是判断而非数据复述）与 `## 信息链`（上游来源 → 本页 → 下游实体/对比/打法 的双链推理链）\n- L2_07 的 practices 页须双链到 `[[服装行业竞争格局]]` 或具体品牌实体页（如 `[[cabbeen]]`、`[[peacebird]]`），打通系统设计与品牌数据\n- 同步到 L2/L3 历史目录"
WRITE_NEW_C = "- ⚠️ 每个新建/更新的 concept/practice 页必须含 `## 结论`（2-4 条合成洞察，是判断而非数据复述）与 `## 信息链`（上游来源 → 本页 → 下游实体/对比/打法 的双链推理链）\n- L2_07 的 practices 页须双链到 `[[服装行业竞争格局]]` 或具体品牌实体页（如 `[[cabbeen]]`、`[[peacebird]]`），打通系统设计与品牌数据\n- ⚠️ **brand_specific 标注（CLAUDE.md 2.5）**：每个新 source 页 frontmatter 必须含 `brand_specific: true/false`——品牌特有数据标 `true`，行业通用方法论标 `false`\n- ⚠️ **superseded_by 回填（CLAUDE.md 2.5）**：写入新 source 时，检查是否有同指标的旧 source，有则在旧 source frontmatter 回填 `superseded_by: \"[[新source]]\"`\n- 同步到 L2/L3 历史目录"

# --- Pattern 2: Add brand_specific to 9.1 confidence section ---
# Insert after the "矛盾检测" line in 9.1
CONF_OLD = "- 矛盾检测（第六步）须优先比对同 `confidence` 等级数据；跨等级冲突以高等级为准，并在页末 `⚠️ 数据矛盾` 注明等级差异。"
CONF_NEW = "- 矛盾检测（第六步）须优先比对同 `confidence` 等级数据；跨等级冲突以高等级为准，并在页末 `⚠️ 数据矛盾` 注明等级差异。\n- **brand_specific 判断**：写入 source 页时，须判断数据为品牌特有（`true`）还是行业通用（`false`），并在页内用 `> **brand_specific**：true/false` 声明。品牌特有 → 双链到品牌实体页；行业通用 → 双链到 concept 页，不链品牌。"

files = {
    "_automation_A1.md": (WRITE_OLD_A, WRITE_NEW_A),
    "_automation_A2.md": (WRITE_OLD_A, WRITE_NEW_A),
    "_automation_A3.md": (WRITE_OLD_A, WRITE_NEW_A),
    "_automation_C.md": (WRITE_OLD_C, WRITE_NEW_C),
}

for fname, (old_w, new_w) in files.items():
    p = BASE / fname
    if not p.exists():
        print(f"  ❌ {fname} not found")
        continue
    t = p.read_text(encoding="utf-8")
    # Write section
    if old_w in t:
        t = t.replace(old_w, new_w)
        print(f"  ✅ {fname} 第四步已插入 brand_specific + superseded_by")
    else:
        print(f"  ⚠️ {fname} 第四步 pattern not found")
    # Confidence section (9.1)
    if CONF_OLD in t:
        t = t.replace(CONF_OLD, CONF_NEW)
        print(f"  ✅ {fname} 9.1节已插入 brand_specific 判断")
    else:
        print(f"  ⚠️ {fname} 9.1节 pattern not found")
    p.write_text(t, encoding="utf-8")

print("\nDone.")
