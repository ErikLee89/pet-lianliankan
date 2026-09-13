# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np
sheet = Image.open("res/bmp_129.png").convert("RGB")
# 看c2几个格子的四角和边缘颜色，判断背景色
for r in [0,4,9,34]:
    cell=np.array(sheet.crop((2*39,r*39,2*39+39,r*39+39))).astype(int)
    corners=[tuple(cell[0,0]),tuple(cell[0,38]),tuple(cell[38,0]),tuple(cell[38,38])]
    print(f"r{r}: 四角颜色={corners}")
# 统计c2 r34的白色占比
cell=np.array(sheet.crop((2*39,34*39,2*39+39,34*39+39))).astype(int)
white=((cell[:,:,0]>200)&(cell[:,:,1]>200)&(cell[:,:,2]>200)).sum()
black=(cell.sum(axis=2)<40).sum()
print(f"c2 r34: 白像素={white}, 纯黑像素={black}, 总={39*39}")
