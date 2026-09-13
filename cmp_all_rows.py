# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np
sheet = Image.open("res/bmp_129.png").convert("RGB")
# 对比c2和c4每一行是否相同
print("c2 vs c4 各行差异:")
same=0; diff=0
for r in range(42):
    a=np.array(sheet.crop((2*39,r*39,2*39+39,r*39+39))).astype(int)
    b=np.array(sheet.crop((4*39,r*39,4*39+39,r*39+39))).astype(int)
    d=((a-b)**2).mean()
    tag="相同" if d<10 else f"差异(d={d:.0f})"
    if d<10: same+=1
    else: diff+=1
    if r<5 or d>=10:
        print(f"  r{r}: {tag}")
print(f"\n相同:{same}行, 不同:{diff}行")
