import sys
from markitdown import MarkItDown
md = MarkItDown()
r = md.convert(r"C:\Users\Administrator\Desktop\培训课件\初级\卖场管理\卖场建设8大项（1603）.xlsx")
open(r"D:\Fashion Doctor\fashion-doctor\knowledge_base\human\培训课件\初级\卖场管理\卖场建设8大项（1603）.md", "w", encoding="utf-8").write(r.text_content)
