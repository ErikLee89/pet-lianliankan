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
seen = {}
for r in range(7):
    for c in range(12):
        a = np.array(img.crop((xs[c]+3, ys[r]+3, xs[c]+37, ys[r]+47))).astype(float)
        d = [((a - ra)**2).mean() for ra in ref_arr]
        v = int(np.argmin(d))
        if min(d) < 15000:
            seen.setdefault(v, []).append((r, c))
pairs = sorted(seen)
# 每个图案：上面2张截图，下面2张不同参考图
CW, CH = 44, 50
H = CH*4 + 30
canvas = Image.new("RGB", (len(pairs)*CW, H), (30, 30, 30))
dr = ImageDraw.Draw(canvas)
for k, v in enumerate(pairs):
    x = k*CW
    shots = seen[v][:2]
    for n, (r, c) in enumerate(shots):
        shot = img.crop((xs[c]+3, ys[r]+3, xs[c]+37, ys[r]+47))
        canvas.paste(shot, (x+5, 14 + n*(CH-6)))
    # 取两个不同参考图
    cand = [i for i in [v, (v+21) % 42]]
    for n, ci in enumerate(cand):
        ref = refs[ci].resize((30, 40), Image.NEAREST)
        canvas.paste(ref, (x+7, 14 + 2*(CH-6) + 4 + n*(CH-14)))
    dr.text((x+16, 2), str(v), fill=(255,255,0))
canvas = canvas.resize((canvas.width*2, canvas.height*2), Image.NEAREST)
canvas.save("compare3.png")
print("OUTPUT=" + __import__("os").path.abspath("compare3.png"))
