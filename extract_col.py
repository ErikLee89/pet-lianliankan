# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np, os
sheet = Image.open("res/bmp_129.png").convert("RGB")

def extract(col, outdir):
    os.makedirs(outdir, exist_ok=True)
    for r in range(42):
        cell = sheet.crop((col*39, r*39, col*39+39, r*39+39))
        arr = np.array(cell)
        # 黑底转透明
        alpha = np.where(arr.sum(axis=2, keepdims=True)>40, 255, 0).astype(np.uint8)
        rgba = np.dstack([arr, alpha])
        Image.fromarray(rgba, "RGBA").save(f"{outdir}/pet_{r:02d}.png")

# 提取 c0 和 c2 两套
extract(0, "col0_tiles")
extract(2, "col2_tiles")

# 生成瓢虫(r32,33,34)的三列对比图
rows=[32,33,34]
canvas=Image.new("RGB",(3*60+10, 3*70+10),(30,30,30))
from PIL import ImageDraw
dr=ImageDraw.Draw(canvas)
labels=["c0","c2","c4(现用)"]
for ci,col in enumerate([0,2,4]):
    for ri,r in enumerate(rows):
        cell=sheet.crop((col*39,r*39,col*39+39,r*39+39))
        canvas.paste(cell.resize((54,54),Image.NEAREST),(ci*60+6, ri*70+16))
        dr.text((ci*60+24, ri*70+4), labels[ci], fill=(255,255,0))
canvas=canvas.resize((canvas.width*3,canvas.height*3),Image.NEAREST)
canvas.save("ladybug_3col.png")
print("OUTPUT="+os.path.abspath("ladybug_3col.png"))
print("已提取 col0_tiles/ 和 col2_tiles/ 各42张")
