# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np
sheet = Image.open("res/bmp_129.png").convert("RGB")
# 瓢虫在第34行（红600）。分析三列的顶部触角
r=34
for col,name in [(0,'c0'),(2,'c2'),(4,'c4现用')]:
    cell=np.array(sheet.crop((col*39,r*39,col*39+39,r*39+39))).astype(int)
    nonblack=(cell.sum(axis=2)>60)
    # 顶部触角：找最上方的内容像素，看y最小值和顶部细线
    ys,xs=np.where(nonblack)
    top_y=ys.min()
    # 数顶部区域(y < top_y+6)的孤立细线（触角通常很细，每行只有1-3像素）
    antenna_rows=0
    for yy in range(top_y, min(top_y+8,39)):
        rowcount=nonblack[yy].sum()
        if 0<rowcount<=4:  # 细线状=触角
            antenna_rows+=1
    print(f"{name}: 内容顶部y={top_y}, 顶部细线行数(触角特征)={antenna_rows}, 总内容={nonblack.sum()}")
    # 打印顶部10行的每行像素数，直观看触角
    for yy in range(top_y, min(top_y+10,39)):
        bar="#"*nonblack[yy].sum()
        print(f"     y{yy}: {nonblack[yy].sum():2d} {bar}")
    print()
