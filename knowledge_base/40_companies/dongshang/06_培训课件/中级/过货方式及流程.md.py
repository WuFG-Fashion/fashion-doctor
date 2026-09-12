import sys
from markitdown import MarkItDown
md = MarkItDown()
r = md.convert(r"C:\Users\Administrator\Desktop\培训课件\中级\过货方式及流程.pptx")
open(r"D:\Fashion Doctor\fashion-doctor\knowledge_base\human\培训课件\中级\过货方式及流程.md", "w", encoding="utf-8").write(r.text_content)
