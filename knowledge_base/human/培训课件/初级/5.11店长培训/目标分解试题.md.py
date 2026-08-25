import sys
from markitdown import MarkItDown
md = MarkItDown()
r = md.convert(r"C:\Users\Administrator\Desktop\培训课件\初级\5.11店长培训\目标分解试题.xlsx")
open(r"D:\Fashion Doctor\fashion-doctor\knowledge_base\human\培训课件\初级\5.11店长培训\目标分解试题.md", "w", encoding="utf-8").write(r.text_content)
