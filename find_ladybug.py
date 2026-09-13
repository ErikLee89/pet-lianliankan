# -*- coding: utf-8 -*-
from PIL import Image
im = Image.open("bmp_129.png").convert("RGB")
W,H = im.size  # 234 x 1638
print("图集尺寸:", im.size, "列数:", W//39, "行数:", H//39)
# 找瓢虫：红色(R高G低B低)密集的格子
# 逐格统计红色像素数
import math
COLS=W//39; ROWS=H//39
results=[]
for r in range(ROWS):
    for c in range(COLS):
        cell = im.crop((c*39, r*39, c*39+39, r*39+39))
        px = list(cell.getdata())
        red = sum(1 for p in px if p[0]>150 and p[1]<90 and p[2]<90)
        results.append((red, r, c))
results.sort(reverse=True)
print("红色最多的前6格(红色像素数,行,列):")
for red,r,c in results[:6]:
    print(f"  格[{r}][{c}] 红像素={red}  → 图标序号(按行优先)={r*COLS+c}")
