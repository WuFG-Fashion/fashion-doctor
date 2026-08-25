import sys
from markitdown import MarkItDown
md = MarkItDown()
r = md.convert(r"D:\Fashion Doctor\fashion-doctor\knowledge_base\human\.conv_tmp\卖场氛围营造（1603）.docx")
open(r"D:\Fashion Doctor\fashion-doctor\knowledge_base\human\培训课件\初级\卖场管理\卖场氛围营造（1603）.md", "w", encoding="utf-8").write(r.text_content)
