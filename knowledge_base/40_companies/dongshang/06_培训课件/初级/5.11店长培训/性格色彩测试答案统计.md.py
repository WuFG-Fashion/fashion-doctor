import sys
from markitdown import MarkItDown
md = MarkItDown()
r = md.convert(r"D:\Fashion Doctor\fashion-doctor\knowledge_base\human\.conv_tmp\性格色彩测试答案统计.docx")
open(r"D:\Fashion Doctor\fashion-doctor\knowledge_base\human\培训课件\初级\5.11店长培训\性格色彩测试答案统计.md", "w", encoding="utf-8").write(r.text_content)
