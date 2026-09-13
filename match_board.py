# -*- coding: utf-8 -*-
# 对每个格子，和42张参考图逐一比对；同时把"格子图 + 最佳参考 + 次佳参考"并排导出验证
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

board = []
for r in range(7):
    row = []
    for c in range(12):
        a = np.array(img.crop((xs[c]+3, ys[r]+3, xs[c]+37, ys[r]+47))).astype(float)
        d = np.array([((a - ra)**2).mean() for ra in ref_arr])
        top2 = np.argsort(d)[:2]
        row.append((int(top2[0]), int(d[top2[0]]), int(top2[1]), int(d[top2[1]])))
    board.append(row)

# 输出每个格子 最优/次优 及差距（差距小说明易混淆）
print("每格: 最优(误差) 次优(误差)")
for r in range(7):
    for c in range(12):
        b, be, s, se = board[r][c]
        flag = " <-- 接近" if se - be < 2500 else ""
        print(f"r{r}c{c:02d}: #{b:02d}({be}) #{s:02d}({se}){flag}")
