# -*- coding: utf-8 -*-
import numpy as np, os
from PIL import Image, ImageDraw
SHOT = r"C:\Users\Erik\AppData\Local\Temp\comate_app_clipboard\image_aa60d7aa.png"
img = Image.open(SHOT).convert("RGB")
xs = [162 + 40*c for c in range(12)]
ys = [160 + 50*r for r in range(8)]
cells = []
for r in range(7):
    for c in range(12):
        a = np.array(img.crop((xs[c]+3, ys[r]+3, xs[c]+37, ys[r]+47))).astype(float)
        cells.append(((r, c), a))
# 聚类：误差小于阈值视为同组
groups = []
for pos, a in cells:
    for g in groups:
        if ((a - g["rep"])**2).mean() < 1200:
            g["cells"].append((pos, a))
            break
    else:
        groups.append({"rep": a, "cells": [(pos, a)]})
print("聚类数:", len(groups))
for gi, g in enumerate(sorted(groups, key=lambda x: -len(x["cells"]))):
    print(f"组{gi}: {len(g['cells'])}格 at {[p for p,_ in g['cells']]}")
# 每组导出一张验证图：放大首格
os.makedirs("clusters", exist_ok=True)
for gi, g in enumerate(groups):
    strip = Image.new("RGB", (len(g['cells'])*46 + 50, 56), (15,15,15))
    dr = ImageDraw.Draw(strip)
    dr.text((2,2), f"G{gi}", fill=(255,255,0))
    for k,(pos,a) in enumerate(g['cells']):
        cell = Image.fromarray(a.astype(np.uint8))
        strip.paste(cell, (44 + k*46, 6))
        dr.text((44+k*46+12, 0), f"{pos[0]}{pos[1]:02d}", fill=(200,200,200))
    strip = strip.resize((strip.width*3, strip.height*3), Image.NEAREST)
    strip.save(f"clusters/g_{gi:02d}.png")
print("已导出", len(groups), "组")
