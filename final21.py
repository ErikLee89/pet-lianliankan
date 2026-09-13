# -*- coding: utf-8 -*-
import numpy as np
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
firsts = [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,7),(0,8),(0,9),(0,10),(0,11),
          (1,1),(1,3),(1,4),(1,5),(1,7),(1,10),(2,1),(2,2),(2,4),(2,5)]
CW, CH = 46, 56
# 每行：G编号 + 格子 + 前3名候选参考
canvas = Image.new("RGB", (CW*5, len(firsts)*(CH+8)), (20,20,20))
dr = ImageDraw.Draw(canvas)
result = {}
for gi,(r,c) in enumerate(firsts):
    a = np.array(img.crop((xs[c]+3, ys[r]+3, xs[c]+37, ys[r]+47))).astype(float)
    d = sorted(((i, ((a - ra)**2).mean()) for i, ra in ref_arr.items()), key=lambda x: x[1])
    top3 = [x[0] for x in d[:3]]
    result[gi] = top3
    y = gi*(CH+8)
    dr.text((14, y+2), f"G{gi}", fill=(255,255,0))
    cell = img.crop((xs[c]+3, ys[r]+3, xs[c]+37, ys[r]+47))
    canvas.paste(cell, (6, y+14))
    for k, ci in enumerate(top3):
        canvas.paste(refs[ci], (CW*(k+1)+6, y+14))
        dr.text((CW*(k+1)+20, y+2), str(ci), fill=(0,255,255) if k else (0,255,0))
canvas = canvas.resize((canvas.width*3, canvas.height*3), Image.NEAREST)
canvas.save("final21.png")
print("OUTPUT=" + __import__("os").path.abspath("final21.png"))
for gi, t in result.items(): print(f"G{gi}: {t}")
