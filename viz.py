# -*- coding: utf-8 -*-
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
ids = []
for r in range(8):
    row = []
    for c in range(12):
        a = np.array(img.crop((xs[c]+3, ys[r]+3, xs[c]+37, ys[r]+47))).astype(float)
        best, bd = -1, 1e18
        for i, ra in enumerate(ref_arr):
            d = ((a - ra)**2).mean()
            if d < bd: bd, best = d, i
        row.append(best if bd < 15000 else -1)  # 误差过大视为未识别
    ids.append(row)
# 每张图案凑一对示例格，拼成对比图：左=参考 右=截图
seen = {}
for r in range(8):
    for c in range(12):
        v = ids[r][c]
        if v >= 0 and v not in seen: seen[v] = (r, c)
pairs = sorted(seen)
CW, CH = 40, 50
canvas = Image.new("RGB", (len(pairs)*CW*2, CH + 18), (40, 40, 40))
from PIL import ImageDraw
dr = ImageDraw.Draw(canvas)
for k, v in enumerate(pairs):
    r, c = seen[v]
    ref = refs[v].resize((34, 44), Image.NEAREST)
    shot = img.crop((xs[c]+3, ys[r]+3, xs[c]+37, ys[r]+47))
    canvas.paste(ref, (k*CW*2, 14)); canvas.paste(shot, (k*CW*2+CW, 14))
    dr.text((k*CW*2+6, 2), str(v), fill=(255,255,0))
    dr.text((k*CW*2+CW+6, 2), str(v), fill=(0,255,255))
canvas = canvas.resize((canvas.width*2, canvas.height*2), Image.NEAREST)
canvas.save("compare.png")
print("OUTPUT=" + __import__("os").path.abspath("compare.png"))
print("图案清单:", pairs)
