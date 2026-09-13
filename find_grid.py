# -*- coding: utf-8 -*-
import numpy as np
from PIL import Image
SHOT = r"C:\Users\Erik\AppData\Local\Temp\comate_app_clipboard\image_aa60d7aa.png"
img = np.array(Image.open(SHOT).convert("RGB")).astype(int)
H, W = img.shape[:2]
R, G, B = img[:,:,0], img[:,:,1], img[:,:,2]
# 粉色/品红掩码（原版牌面底色）
pink = (R > 180) & (B > 120) & (R > G + 40) & (B > G + 10)
# 列方向投影：哪一列有多少粉色像素
colsum = pink.sum(axis=0)
rowsum = pink.sum(axis=1)
def spans(arr, thresh):
    out, s = [], None
    for i, v in enumerate(arr):
        if v >= thresh and s is None: s = i
        if v < thresh and s is not None: out.append((s, i-1)); s = None
    if s is not None: out.append((s, len(arr)-1))
    return out
print("粉色列段(>100):", spans(colsum, 100))
print("粉色行段(>100):", spans(rowsum, 100))
print("粉色行段(>200):", spans(rowsum, 200))
print("粉色列段(>200):", spans(colsum, 200))
