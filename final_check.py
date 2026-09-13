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

# 只保留前7行（第8行是空白区）
grid = []
for r in range(7):
    row = []
    for c in range(12):
        a = np.array(img.crop((xs[c]+3, ys[r]+3, xs[c]+37, ys[r]+47))).astype(float)
        d = [((a - ra)**2).mean() for ra in ref_arr]
        row.append((int(np.argmin(d)), float(min(d))))
    grid.append(row)

from collections import Counter
cnt = Counter(v for r in range(7) for c in range(12) for v, dd in [grid[r][c]] if dd < 15000)
ids = sorted(cnt)
print(f"识别格数: {sum(cnt.values())} / 84，应凑成 21 种")
print(f"当前识别: {len(ids)} 种 -> {ids}")
print("次数:", dict(sorted(cnt.items())))

# 每个图案拿4张实际出现位置，验证是否同物
CW, CH = 46, 52
canvas = Image.new("RGB", (len(ids)*CW, CH*4+20), (25,25,25))
dr = ImageDraw.Draw(canvas)
for k, v in enumerate(ids):
    x = k*CW
    locs = [(r,c) for r in range(7) for c in range(12) if grid[r][c][0]==v and grid[r][c][1]<15000][:4]
    for n,(r,c) in enumerate(locs):
        shot = img.crop((xs[c]+3, ys[r]+3, xs[c]+37, ys[r]+47))
        canvas.paste(shot, (x+6, 14+n*(CH-4)))
    dr.text((x+18, 2), str(v), fill=(255,255,0))
canvas = canvas.resize((canvas.width*2, canvas.height*2), Image.NEAREST)
canvas.save("final_check.png")
print("OUTPUT=" + __import__("os").path.abspath("final_check.png"))
