import sys
from markitdown import MarkItDown
md = MarkItDown()
r = md.convert(r"C:\Users\Administrator\Desktop\店铺制度\前台销售输机管理.docx")
open(r"D:\Fashion Doctor\fashion-doctor\knowledge_base\human\店铺制度\前台销售输机管理.md", "w", encoding="utf-8").write(r.text_content)
