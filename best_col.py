# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np
sheet = Image.open("res/bmp_129.png").convert("RGB")
# 对每一行，比较c0/c2/c4三列的内容量，看哪列更完整
print("每行 c0/c2/c4 内容像素对比(标*为最多):")
wins={0:0,2:0,4:0}
for r in range(42):
    vals={}
    for c in [0,2,4]:
        cell=np.array(sheet.crop((c*39,r*39,c*39+39,r*39+39))).astype(int)
        vals[c]=(cell.sum(axis=2)>60).sum()
    mx=max(vals,key=vals.get)
    wins[mx]+=1
    if r in (31,32,33,34) or r<3:
        print(f"  r{r}: c0={vals[0]} c2={vals[2]} c4={vals[4]}  → 最多:c{mx}")
print("42行中各列'最完整'次数:",wins)
