import sys
from markitdown import MarkItDown
md = MarkItDown()
r = md.convert(r"C:\Users\Administrator\Desktop\店铺制度\卡宾卖场规范30条.docx")
open(r"D:\Fashion Doctor\fashion-doctor\knowledge_base\human\店铺制度\卡宾卖场规范30条.md", "w", encoding="utf-8").write(r.text_content)
