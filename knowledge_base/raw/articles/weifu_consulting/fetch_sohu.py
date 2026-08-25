# -*- coding: utf-8 -*-
"""抓取韦孚咨询搜狐号全部文章 → Markdown + 图片清单
用法: python fetch_sohu.py
"""
import json, os, re, time, sys
import urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "md")
IMG = os.path.join(BASE, "images")
os.makedirs(OUT, exist_ok=True)
os.makedirs(IMG, exist_ok=True)

UA = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Referer": "https://www.sohu.com/",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

ARTICLES = [
    (534829270, "2022-04-13", "韦孚咨询×艾诺丝雅诗-3C年度商品经营体系战略合作"),
    (535937705, "2022-04-13", "地素时尚年度3C经营体系战略合作"),
    (535958856, "2022-04-13", "卡尔丹顿2022春夏设计企划项目辅导"),
    (536492480, "2022-04-13", "秋水伊人2022夏秋设计企划项目辅导"),
    (536498162, "2022-04-13", "日播全渠道目标增量标杆体系"),
    (534521337, "2022-04-01", "疫情常态化下服装行业实体门店要怎么活下去"),
    (534126572, "2022-03-31", "3C品牌经营方案研究中心"),
    (534107127, "2022-03-31", "基于核心顾客大企划增量方案"),
    (471387379, "2021-06-10", "6月底限定咨询课已开启来跟炳哥一起探寻业绩增量秘诀"),
    (467523956, "2021-05-20", "李炳辰3C商品零售体系"),
    (465944269, "2021-05-12", "歌力思珂莱蒂尔等品牌高管齐聚玛克茜妮"),
    (461781409, "2021-04-20", "安踏集团如何实现2025年集团双千亿的目标"),
    (459206347, "2021-04-06", "杭州站3C经营体系咨询公开课落地行动"),
    (453905487, "2021-03-04", "销售联动订货-3C经营复盘"),
    (453804049, "2021-03-03", "2021品牌增量规划公开课现场回顾上海站"),
    (299880865, "2019-03-08", "色盲与色盲测试"),
    (202802601, "2017-11-07", "2017潘通流行色绿Greenery"),
    (202798499, "2017-11-07", "为何品牌纷纷往商品上添加经典图案或短语"),
    (202789857, "2017-11-07", "潘通色紫LoveSymbolNo2"),
    (202789335, "2017-11-07", "时尚轮回牛仔面料袭卷NYFW2018SS"),
    (201128282, "2017-10-30", "韦孚国际美学零售新模式专注服饰行业的咨询服务运营商"),
]


def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="ignore")


def strip_tags(html):
    html = re.sub(r"<script[\s\S]*?</script>", "", html)
    html = re.sub(r"<style[\s\S]*?</style>", "", html)
    # 段落/换行标签转为换行
    html = re.sub(r"</(p|div|h[1-6]|li|tr|br)>", "\n", html)
    html = re.sub(r"<(br|p|div|li|tr|h[1-6])[^>]*>", "\n", html)
    text = re.sub(r"<[^>]+>", "", html)
    text = text.replace("&nbsp;", " ").replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"').replace("&#39;", "'")
    lines = [l.strip() for l in text.split("\n")]
    lines = [l for l in lines if l]
    return "\n".join(lines)


def extract_article(html):
    """提取标题、正文、图片"""
    title = ""
    m = re.search(r"<title>(.*?)</title>", html, re.S)
    if m:
        title = m.group(1).strip()
    # 正文容器
    body = ""
    for pat in [r'<article[^>]*>([\s\S]*?)</article>',
                r'class="article[^"]*"[^>]*>([\s\S]*?)</div>']:
        m = re.search(pat, html)
        if m:
            body = m.group(1)
            break
    if not body:
        m = re.search(r'id="mp-editor"[\s\S]*?</div>', html)
        body = m.group(0) if m else html
    text = strip_tags(body)
    # 图片
    imgs = re.findall(r'<img[^>]+src="([^"]+)"', body)
    return title, text, imgs


def main():
    results = {}
    for aid, date, name in ARTICLES:
        url = f"https://www.sohu.com/a/{aid}_100049954"
        fn = f"{date}_{aid}_{name}.md"
        try:
            html = fetch(url)
            title, text, imgs = extract_article(html)
            md = f"# {title}\n\n> 来源: {url}\n> 抓取日期: 2026-08-25\n\n" + text
            with open(os.path.join(OUT, fn), "w", encoding="utf-8") as f:
                f.write(md)
            results[fn] = {"url": url, "title": title, "text_len": len(text), "imgs": len(imgs)}
            print(f"OK  {fn}  text={len(text)} imgs={len(imgs)}")
        except Exception as e:
            results[fn] = {"url": url, "error": str(e)}
            print(f"ERR {fn}  {e}")
        time.sleep(1.5)
    with open(os.path.join(BASE, "fetch_result.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
