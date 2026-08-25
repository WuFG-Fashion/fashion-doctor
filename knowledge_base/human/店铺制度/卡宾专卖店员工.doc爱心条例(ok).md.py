import sys
from markitdown import MarkItDown
md = MarkItDown()
r = md.convert(r"D:\Fashion Doctor\fashion-doctor\knowledge_base\human\.conv_tmp\卡宾专卖店员工.doc爱心条例(ok).docx")
open(r"D:\Fashion Doctor\fashion-doctor\knowledge_base\human\店铺制度\卡宾专卖店员工.doc爱心条例(ok).md", "w", encoding="utf-8").write(r.text_content)
