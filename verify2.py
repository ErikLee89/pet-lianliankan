# -*- coding: utf-8 -*-
# 针对4个存疑组，导出：格子 + 所有形状相似的候选参考图
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
    refs[i] = bg.convert("RGB").resize((40, 52), Image.LANCZOS)
# 存疑：G13(绿色虫)、G15(棕色)、G10(粉色)、G12(粉色)
cases = {
    "G13 绿虫@1,4": (1, 4),
    "G15 棕色@1,7": (1, 7),
    "G10 粉@0,11": (0, 11),
    "G12 粉@1,3": (1, 3),
}
CW, CH = 56, 66
canvas = Image.new("RGB", (CW*8, len(cases)*(CH+16)), (20,20,20))
dr = ImageDraw.Draw(canvas)
for row, (label, (r, c)) in enumerate(cases.items()):
    y = row*(CH+16)
    a = np.array(img.crop((xs[c]+3, ys[r]+3, xs[c]+37, ys[r]+47)).resize((40,52), Image.LANCZOS)).astype(float)
    cell = img.crop((xs[c]+3, ys[r]+3, xs[c]+37, ys[r]+47)).resize((40,52), Image.NEAREST)
    dr.text((10, y+2), label, fill=(255,255,0))
    canvas.paste(cell, (8, y+12))
    # 找误差最小的前7个
    d = sorted(((i, ((a - np.array(refs[i]).astype(float))**2).mean()) for i in refs), key=lambda x: x[1])[:7]
    for k, (ci, err) in enumerate(d):
        canvas.paste(refs[ci], (CW*(k+1)+8, y+12))
        dr.text((CW*(k+1)+18, y+2), f"{ci}", fill=(0,255,0) if k==0 else (150,150,150))
canvas = canvas.resize((canvas.width*3, canvas.height*3), Image.NEAREST)
canvas.save("verify2.png")
print("OUTPUT=" + __import__("os").path.abspath("verify2.png"))
