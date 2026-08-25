import sys
from markitdown import MarkItDown
md = MarkItDown()
r = md.convert(r"C:\Users\Administrator\Desktop\培训课件\初级\6.3店助培训\店助岗位职责.docx")
open(r"D:\Fashion Doctor\fashion-doctor\knowledge_base\human\培训课件\初级\6.3店助培训\店助岗位职责.md", "w", encoding="utf-8").write(r.text_content)
