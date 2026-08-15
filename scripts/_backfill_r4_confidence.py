# 回填空量 R4 的 11 个 source 页 confidence（按品牌性质分级）
import os

base = "knowledge_base/wiki/sources/"
# (文件名子串, 置信度)
mapping = [
    ("R4_卡宾", "财报"),          # cabbeen HK02030 中报
    ("R4_太平鸟", "财报"),        # 和平鸟 中报
    ("R4_楚萨迪", "媒体估算"),    # Trussardi 私企，营收多为媒体/行业推算
    ("R4_卡尔拉格斐", "财报"),    # 七匹狼公告并表口径
    ("R4_萨洛蒙", "财报"),        # Amer Sports 财报
    ("R4_卡骆驰", "财报"),        # Crocs Inc 财报
    ("R4_MLB_FF", "财报"),        # F&F 韩国上市财报
    ("R4_2AM", "品牌自宣"),       # 卡宾青年线 3D 鞋为品牌 PR
    ("R4_CHUU", "媒体估算"),      # 中国运营多为媒体/行业推算
    ("R4_艾诺丝", "品牌自宣"),    # 私企女装，官网/通稿口径
    ("R4_迪卡轩", "品牌自宣"),    # 私企女装，官网/通稿口径
]

for key, conf in mapping:
    cands = [f for f in os.listdir(base) if key in f and f.endswith(".md")]
    assert len(cands) == 1, (key, cands)
    fn = base + cands[0]
    s = open(fn, encoding="utf-8").read()

    # frontmatter：按首个 '---\n' 拆分
    parts = s.split("---\n", 2)
    assert len(parts) == 3, (fn, "frontmatter split failed")
    fm = parts[1]
    if "confidence:" not in fm:
        fm = fm.rstrip() + f"\nconfidence: {conf}\n"
    s2 = "---\n" + fm + "---\n" + parts[2]

    # 页内声明：避免重复
    decl = f"> **置信度**：{conf}\n\n"
    if decl.strip() not in s2:
        if "## 来源链接" in s2:
            s2 = s2.replace("## 来源链接", decl + "## 来源链接", 1)
        elif "## 核心要点" in s2:
            s2 = s2.replace("## 核心要点", decl + "## 核心要点", 1)

    open(fn, "w", encoding="utf-8").write(s2)
    print("updated", cands[0], "->", conf)
