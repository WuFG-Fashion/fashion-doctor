import sys
from markitdown import MarkItDown
md = MarkItDown()
r = md.convert(r"C:\Users\Administrator\Desktop\培训课件\中级\1.3金牌店长特训营之会议管理篇.pptx")
open(r"D:\Fashion Doctor\fashion-doctor\knowledge_base\human\培训课件\中级\1.3金牌店长特训营之会议管理篇.md", "w", encoding="utf-8").write(r.text_content)
