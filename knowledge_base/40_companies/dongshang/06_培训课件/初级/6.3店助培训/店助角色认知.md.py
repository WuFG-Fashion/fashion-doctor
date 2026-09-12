import sys
from markitdown import MarkItDown
md = MarkItDown()
r = md.convert(r"C:\Users\Administrator\Desktop\培训课件\初级\6.3店助培训\店助角色认知.pptx")
open(r"D:\Fashion Doctor\fashion-doctor\knowledge_base\human\培训课件\初级\6.3店助培训\店助角色认知.md", "w", encoding="utf-8").write(r.text_content)
