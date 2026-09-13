# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np
sheet = Image.open("res/bmp_129.png").convert("RGB")
# 瓢虫最可能在红色最多的行：34和32行。对比这两行的每一列
for r in [32,34]:
    print(f"\n=== 第{r}行 各列图标分析 ===")
    for c in range(6):
        cell=np.array(sheet.crop((c*39,r*39,c*39+39,r*39+39))).astype(int)
        # 非黑像素(图标内容)
        nonblack=(cell.sum(axis=2)>60)
        # 内容边界框
        if nonblack.sum()>0:
            ys,xs=np.where(nonblack)
            bbox=(xs.min(),ys.min(),xs.max(),ys.max())
            red=((cell[:,:,0]>150)&(cell[:,:,1]<90)&(cell[:,:,2]<90)).sum()
            # 顶部2行是否有内容（触角）
            top_content=nonblack[:4,:].sum()
            print(f"  c{c}: 内容bbox={bbox} 红像素={red} 顶部4行像素数={top_content} 内容总数={nonblack.sum()}")
