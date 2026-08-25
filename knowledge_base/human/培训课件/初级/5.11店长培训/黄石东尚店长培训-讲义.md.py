import sys
from markitdown import MarkItDown
md = MarkItDown()
r = md.convert(r"C:\Users\Administrator\Desktop\培训课件\初级\5.11店长培训\黄石东尚店长培训-讲义.docx")
open(r"D:\Fashion Doctor\fashion-doctor\knowledge_base\human\培训课件\初级\5.11店长培训\黄石东尚店长培训-讲义.md", "w", encoding="utf-8").write(r.text_content)
