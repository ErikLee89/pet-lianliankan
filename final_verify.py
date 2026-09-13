# -*- coding: utf-8 -*-
import numpy as np
from PIL import Image, ImageDraw
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

def cell_err(r, c):
    a = np.array(img.crop((xs[c]+3, ys[r]+3, xs[c]+37, ys[r]+47))).astype(float)
    d = [((a - ra)**2).mean() for ra in ref_arr]
    return d

# 前7行84格，21种图案。先用自动识别结果，再人工修正3种
# 自动识别
board = []
for r in range(7):
    row = []
    for c in range(12):
        d = cell_err(r, c)
        row.append(int(np.argmin(d)))
    board.append(row)

# 打印识别出的图案分布位置，便于人工核对
from collections import defaultdict
pos = defaultdict(list)
for r in range(7):
    for c in range(12):
        pos[board[r][c]].append((r, c))
print("自动识别分布:")
for v in sorted(pos):
    print(f"  #{v}: {len(pos[v])}次 at {pos[v][:6]}")

# 对每个识别结果，取它出现次数第2、3、4少的候选图案对比
# 输出每个图案的前4名候选误差
print("\n每个格子的Top3候选（误差）:")
for r in range(7):
    line = []
    for c in range(12):
        d = cell_err(r, c)
        top = np.argsort(d)[:3]
        line.append("/".join(f"{int(t)}:{int(d[t])//1000}k" for t in top))
    print(" ".join(f"{s:22s}" for s in line))
