# -*- coding: utf-8 -*-
"""从搜狐文章页 cfgs JSON 中提取真实图片URL并下载到 images/<aid>/"""
import os, re, time
import urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(BASE, "images")
os.makedirs(IMG, exist_ok=True)

UA = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Referer": "https://www.sohu.com/",
}

AIDS = [
    534829270, 535937705, 535958856, 536492480, 536498162, 534521337,
    534126572, 534107127, 471387379, 467523956, 465944269, 461781409,
    459206347, 453905487, 453804049, 299880865, 202802601, 202798499,
    202789857, 202789335, 201128282,
]

def fetch_text(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "ignore")

def fetch_bytes(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read()

def main():
    total = 0
    for aid in AIDS:
        url = f"https://www.sohu.com/a/{aid}_100049954"
        try:
            html = fetch_text(url)
        except Exception as e:
            print("ERR fetch", aid, e); continue
        # 提取 cfgs JSON 里的图片 url（p*.itc.cn/images0x/...）
        urls = re.findall(r'"url":\s*"(https://p\d+\.itc\.cn/[^"]+)"', html)
        # 去重保序
        seen, uniq = set(), []
        for u in urls:
            if u not in seen:
                seen.add(u); uniq.append(u)
        if not uniq:
            print("no imgs for", aid); continue
        d = os.path.join(IMG, str(aid))
        os.makedirs(d, exist_ok=True)
        n = 0
        for u in uniq:
            ext = os.path.splitext(u.split("?")[0])[1].lower()
            if ext not in (".jpg", ".jpeg", ".png", ".gif", ".webp"):
                ext = ".jpg"
            out = os.path.join(d, f"img_{n+1}{ext}")
            if os.path.exists(out):
                n += 1; continue
            try:
                data = fetch_bytes(u)
                if len(data) > 2000:
                    with open(out, "wb") as f:
                        f.write(data)
                    n += 1; total += 1
            except Exception:
                pass
        print("aid", aid, "found", len(uniq), "saved", n)
        time.sleep(1.0)
    print("TOTAL saved:", total)

if __name__ == "__main__":
    main()
