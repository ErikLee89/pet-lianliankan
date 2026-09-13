# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np
sheet = Image.open("res/bmp_129.png").convert("RGB")
r=34; col=4  # c4 瓢虫
cell=np.array(sheet.crop((col*39,r*39,col*39+39,r*39+39))).astype(int)
print("c4瓢虫 完整像素图(.=黑背景, 字母=颜色):")
for y in range(39):
    line=""
    for x in range(39):
        R,G,B=cell[y,x]
        s=R+G+B
        if s<40: line+="."
        elif R>150 and G<90 and B<90: line+="R"  # 红
        elif R>180 and G>180 and B>180: line+="W"  # 白
        elif abs(R-G)<30 and abs(G-B)<30: line+="g"  # 灰
        else: line+="#"
    print(f"{y:2d} {line}")
# 检查顶部区域是否有"非黑但也不是深色"的触角像素
print("\n顶部y0-6的非纯黑像素(可能触角):")
for y in range(0,8):
    for x in range(39):
        R,G,B=cell[y,x]
        if R+G+B>=40:
            print(f"  y{y} x{x}: RGB=({R},{G},{B})")
