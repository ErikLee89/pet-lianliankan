# -*- coding: utf-8 -*-
from PIL import Image
import os
SHOT = r"C:\Users\Erik\AppData\Local\Temp\comate_app_clipboard\image_aa60d7aa.png"
img = Image.open(SHOT).convert("RGB")
xs = [162 + 40*c for c in range(12)]
ys = [160 + 50*r for r in range(8)]
os.makedirs("cells_raw", exist_ok=True)
for r in range(7):
    for c in range(12):
        cell = img.crop((xs[c]+3, ys[r]+3, xs[c]+37, ys[r]+47))
        cell = cell.resize((cell.width*5, cell.height*5), Image.NEAREST)
        cell.save(f"cells_raw/r{r}_c{c:02d}.png")
print("84格导出完成")
