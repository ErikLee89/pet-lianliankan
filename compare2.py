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
# 收集每个图案的前2张示例
seen = {}
for r in range(7):
    for c in range(12):
        a = np.array(img.crop((xs[c]+3, ys[r]+3, xs[c]+37, ys[r]+47))).astype(float)
        d = [((a - ra)**2).mean() for ra in ref_arr]
        v = int(np.argmin(d))
        if min(d) < 15000:
            seen.setdefault(v, []).append((r, c))
pairs = sorted(seen)
CW, CH, ROW = 40, 50, 2
canvas = Image.new("RGB", (len(pairs)*CW*2, (CH+16)*ROW), (30, 30, 30))
dr = ImageDraw.Draw(canvas)
for k, v in enumerate(pairs):
    for n, (r, c) in enumerate(seen[v][:2]):
        shot = img.crop((xs[c]+3, ys[r]+3, xs[c]+37, ys[r]+47))
        canvas.paste(shot, (k*CW*2 + (n % 2)*CW, 14 + (n // 2)*(CH+16)))
    ref = refs[v].resize((34, 44), Image.NEAREST)
    canvas.paste(ref, (k*CW*2, 14 + CH + 16))
    dr.text((k*CW*2+12, 2), str(v), fill=(255,255,0))
    dr.text((k*CW*2+12, 2 + CH + 16), str(v), fill=(0,255,255))
canvas = canvas.resize((canvas.width*2, canvas.height*2), Image.NEAREST)
canvas.save("compare2.png")
print("OUTPUT=" + __import__("os").path.abspath("compare2.png"))
