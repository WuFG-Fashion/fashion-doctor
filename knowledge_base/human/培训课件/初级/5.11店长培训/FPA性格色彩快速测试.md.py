import sys
from markitdown import MarkItDown
md = MarkItDown()
r = md.convert(r"D:\Fashion Doctor\fashion-doctor\knowledge_base\human\.conv_tmp\FPA性格色彩快速测试.docx")
open(r"D:\Fashion Doctor\fashion-doctor\knowledge_base\human\培训课件\初级\5.11店长培训\FPA性格色彩快速测试.md", "w", encoding="utf-8").write(r.text_content)
