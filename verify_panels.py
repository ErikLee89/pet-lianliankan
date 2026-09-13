# -*- coding: utf-8 -*-
import numpy as np, os
from PIL import Image, ImageDraw
SHOT = r"C:\Users\Erik\AppData\Local\Temp\comate_app_clipboard\image_aa60d7aa.png"
img = Image.open(SHOT).convert("RGB")
xs = [162 + 40*c for c in range(12)]
ys = [160 + 50*r for r in range(8)]
refs = {}
for i in range(42):
    im = Image.open(f"assets/tiles/pet_{i:02d}.png").convert("RGBA")
    bg = Image.new("RGBA", im.size, (255, 200, 225, 255))
    bg.alpha_composite(im)
    refs[i] = bg.convert("RGB").resize((34, 44), Image.LANCZOS)
ref_arr = {i: np.array(refs[i]).astype(float) for i in refs}
# 自动识别
board = []
for r in range(7):
    row = []
    for c in range(12):
        a = np.array(img.crop((xs[c]+3, ys[r]+3, xs[c]+37, ys[r]+47))).astype(float)
        d = [(i, ((a - ra)**2).mean()) for i, ra in ref_arr.items()]
        row.append(min(d, key=lambda x: x[1])[0])
    board.append(row)
# 按识别结果分组，每组输出 参考图 + 所有实例
os.makedirs("verify", exist_ok=True)
from collections import defaultdict
pos = defaultdict(list)
for r in range(7):
    for c in range(12):
        pos[board[r][c]].append((r, c))
for v, locs in sorted(pos.items()):
    n = len(locs)
    W = (n + 1) * 46 + 10
    strip = Image.new("RGB", (W, 62), (15, 15, 15))
    dr = ImageDraw.Draw(strip)
    dr.text((2, 2), f"#{v} x{n}", fill=(255, 255, 0))
    strip.paste(refs[v], (4, 14))  # 参考图
    for k, (r, c) in enumerate(locs):
        cell = img.crop((xs[c]+3, ys[r]+3, xs[c]+37, ys[r]+47))
        strip.paste(cell, (50 + k*46, 14))
        dr.text((50 + k*46 + 12, 0), f"{r}{c}", fill=(200, 200, 200))
    strip = strip.resize((strip.width*3, strip.height*3), Image.NEAREST)
    strip.save(f"verify/v_{v:02d}.png")
print("生成", len(pos), "张验证图")
