# -*- coding: utf-8 -*-
from PIL import Image
import os
SHOT = r"C:\Users\Erik\AppData\Local\Temp\comate_app_clipboard\image_aa60d7aa.png"
img = Image.open(SHOT).convert("RGB")
xs = [162 + 40*c for c in range(12)]
ys = [160 + 50*r for r in range(8)]
os.makedirs("rows", exist_ok=True)
for r in range(7):
    strip = Image.new("RGB", (12*46, 56), (15,15,15))
    for c in range(12):
        cell = img.crop((xs[c]+3, ys[r]+3, xs[c]+37, ys[r]+47))
        strip.paste(cell, (c*46+6, 6))
    strip = strip.resize((strip.width*3, strip.height*3), Image.NEAREST)
    strip.save(f"rows/row{r}.png")
print("7行导出完成")
