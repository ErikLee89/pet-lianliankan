# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np
sheet = Image.open("res/bmp_129.png").convert("RGB")
# 在c4里找红色甲虫状（红色为主、带黑点）
print("c4各图标红色像素数(找瓢虫):")
reds=[]
for i in range(42):
    cell=np.array(sheet.crop((4*39,i*39,4*39+39,i*39+39))).astype(int)
    red=((cell[:,:,0]>150)&(cell[:,:,1]<90)&(cell[:,:,2]<90)).sum()
    dark=(cell.sum(axis=2)<60).sum()
    reds.append((red,i))
reds.sort(reverse=True)
for red,i in reds[:6]:
    print(f"  #{i}: 红像素={red}")
