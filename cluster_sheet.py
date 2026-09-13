# -*- coding: utf-8 -*-
import numpy as np
from PIL import Image, ImageDraw
SHOT = r"C:\Users\Erik\AppData\Local\Temp\comate_app_clipboard\image_aa60d7aa.png"
img = Image.open(SHOT).convert("RGB")
xs = [162 + 40*c for c in range(12)]
ys = [160 + 50*r for r in range(8)]
# 每组的首格
firsts = [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,7),(0,8),(0,9),(0,10),(0,11),
          (1,1),(1,3),(1,4),(1,5),(1,7),(1,10),(2,1),(2,2),(2,4),(2,5)]
cols = 7
CW, CH = 60, 70
rows = (len(firsts)+cols-1)//cols
canvas = Image.new("RGB", (cols*CW, rows*(CH+16)), (25,25,25))
dr = ImageDraw.Draw(canvas)
for gi,(r,c) in enumerate(firsts):
    cell = img.crop((xs[c]+3, ys[r]+3, xs[c]+37, ys[r]+47))
    cell = cell.resize((48, 60), Image.NEAREST)
    rr, cc = gi // cols, gi % cols
    canvas.paste(cell, (cc*CW+6, rr*(CH+16)+14))
    dr.text((cc*CW+26, rr*(CH+16)), f"G{gi}", fill=(255,255,0))
canvas = canvas.resize((canvas.width*2, canvas.height*2), Image.NEAREST)
canvas.save("cluster_sheet.png")
print("OUTPUT=" + __import__("os").path.abspath("cluster_sheet.png"))
