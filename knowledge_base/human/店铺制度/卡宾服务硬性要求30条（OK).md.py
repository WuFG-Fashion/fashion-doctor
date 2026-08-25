import sys
from markitdown import MarkItDown
md = MarkItDown()
r = md.convert(r"D:\Fashion Doctor\fashion-doctor\knowledge_base\human\.conv_tmp\卡宾服务硬性要求30条（OK).docx")
open(r"D:\Fashion Doctor\fashion-doctor\knowledge_base\human\店铺制度\卡宾服务硬性要求30条（OK).md", "w", encoding="utf-8").write(r.text_content)
