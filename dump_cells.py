# -*- coding: utf-8 -*-
# 把每个"自动识别图案"的所有实际格子图逐个导出，供肉眼比对
import numpy as np
from PIL import Image
SHOT = r"C:\Users\Erik\AppData\Local\Temp\comate_app_clipboard\image_aa60d7aa.png"
img = Image.open(SHOT).convert("RGB")
xs = [162 + 40*c for c in range(12)]
ys = [160 + 50*r for r in range(8)]
refs = []
for i in range(42):
    im = Image.open(f"assets/tiles/pet_{i:02d}.png").convert("RGBA")
    bg = Image.new("RGBA", im.size, (255, 200, 225, 255))
    bg.alpha_composite(im)
    refs.append(bg.convert("RGB").resize((34, 44), Image.LANCZOS))
ref_arr = [np.array(r).astype(float) for r in refs]
# 识别
grid = {}
for r in range(7):
    for c in range(12):
        a = np.array(img.crop((xs[c]+3, ys[r]+3, xs[c]+37, ys[r]+47))).astype(float)
        d = [((a - ra)**2).mean() for ra in ref_arr]
        grid[(r, c)] = int(np.argmin(d))
# 导出每张识别图的所有实例拼条
import os
os.makedirs("cells", exist_ok=True)
from collections import defaultdict
pos = defaultdict(list)
for k, v in grid.items(): pos[v].append(k)
for v, locs in sorted(pos.items()):
    strip = Image.new("RGB", (len(locs)*40 + 60, 50), (20,20,20))
    strip.paste(refs[v].resize((34,44), Image.NEAREST), (0, 3))  # 最左放参考图
    for n,(r,c) in enumerate(locs):
        strip.paste(img.crop((xs[c]+3, ys[r]+3, xs[c]+37, ys[r]+47)), (60+n*40+3, 3))
    strip = strip.resize((strip.width*3, strip.height*3), Image.NEAREST)
    strip.save(f"cells/id_{v:02d}.png")
print("导出完成，共", len(pos), "种")
