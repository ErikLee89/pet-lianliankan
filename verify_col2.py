# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np
sheet = Image.open("res/bmp_129.png").convert("RGB")
# 检查第2列42行：每行内容量，确认都是有效图标
print("第2列(c2) 42行内容统计:")
empty=0
for r in range(42):
    cell=np.array(sheet.crop((2*39,r*39,2*39+39,r*39+39))).astype(int)
    nonblack=(cell.sum(axis=2)>60).sum()
    flag="" if nonblack>100 else "  <-- 内容过少"
    if nonblack<=100: empty+=1
    if r%6==0 or nonblack<=100:
        print(f"  r{r}: 内容像素={nonblack}{flag}")
print(f"内容过少的行数: {empty}")

# 也检查其他列，看哪列是"完整彩色"的主图集
print("\n各列平均内容像素(前42行):")
for c in range(6):
    tot=0
    for r in range(42):
        cell=np.array(sheet.crop((c*39,r*39,c*39+39,r*39+39))).astype(int)
        tot+=(cell.sum(axis=2)>60).sum()
    print(f"  c{c}: 平均={tot//42}")
