# -*- coding: utf-8 -*-
import numpy as np
from PIL import Image
SHOT = r"C:\Users\Erik\AppData\Local\Temp\comate_app_clipboard\image_aa60d7aa.png"
img = Image.open(SHOT).convert("RGB")
# 精确定位：竖线 x=162..643 (12列, 40px/格)，横线 y=160..560 (8行, 50px/格)
xs = [162 + 40*c for c in range(12)]
ys = [160 + 50*r for r in range(8)]
# 每格去掉边框后图案区域: 宽34(162+3..162+37), 高44(160+3..160+47)
refs = []
for i in range(42):
    im = Image.open(f"assets/tiles/pet_{i:02d}.png").convert("RGBA")
    bg = Image.new("RGBA", im.size, (255, 200, 225, 255))  # 模拟粉格底
    bg.alpha_composite(im)
    refs.append(bg.convert("RGB").resize((34, 44), Image.LANCZOS))
ref_arr = [np.array(r).astype(float) for r in refs]

from collections import Counter
used = Counter(); board = []
for r in range(8):
    row = []
    for c in range(12):
        cell = img.crop((xs[c]+3, ys[r]+3, xs[c]+37, ys[r]+47))
        a = np.array(cell).astype(float)
        # 与42张图比均方差
        best, bd = -1, 1e18
        for i, ra in enumerate(ref_arr):
            d = ((a - ra)**2).mean()
            if d < bd: bd, best = d, i
        row.append((best, int(bd)))
        used[best] += 1
    board.append(row)

print("识别棋盘（编号@误差）:")
for row in board:
    print(" ".join(f"{v:02d}@{d:5d}" for v, d in row))
ids = sorted(used)
print(f"\n不同图标: {len(ids)} 种 -> {ids}")
print("出现次数:", dict(sorted(used.items())))
# 误差分布：真实匹配误差应远小于误配
ds = sorted(d for row in board for _, d in row)
print("误差分布: min", ds[0], "中位", ds[len(ds)//2], "max", ds[-1])
