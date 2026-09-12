import sys
from markitdown import MarkItDown
md = MarkItDown()
r = md.convert(r"C:\Users\Administrator\Desktop\培训课件\初级\6.3店助培训\我是“中级着装顾问-讲师手册.pptx")
open(r"D:\Fashion Doctor\fashion-doctor\knowledge_base\human\培训课件\初级\6.3店助培训\我是“中级着装顾问-讲师手册.md", "w", encoding="utf-8").write(r.text_content)
