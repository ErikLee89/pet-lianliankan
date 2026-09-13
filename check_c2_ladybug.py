# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np
sheet = Image.open("res/bmp_129.png").convert("RGB")
r=34
for col,name in [(2,'c2'),(0,'c0')]:
    cell=np.array(sheet.crop((col*39,r*39,col*39+39,r*39+39))).astype(int)
    print(f"\n=== {name} 第34行 像素图 ===")
    for y in range(39):
        line=""
        for x in range(39):
            R,G,B=cell[y,x]
            s=R+G+B
            if s<40: line+="."
            elif R>150 and G<90 and B<90: line+="R"
            elif R>180 and G>180 and B>180: line+="W"
            elif abs(R-G)<35 and abs(G-B)<35 and s<200: line+="k"  # 深灰/黑
            else: line+="#"
        if line.strip("."):  # 只打印有内容的行
            print(f"{y:2d} {line}")
