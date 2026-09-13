# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw
SHOT = r"C:\Users\Erik\AppData\Local\Temp\comate_app_clipboard\image_aa60d7aa.png"
img = Image.open(SHOT).convert("RGB")
xs = [162 + 40*c for c in range(12)]
ys = [160 + 50*r for r in range(8)]
mapping = {0:0,1:1,2:9,3:37,4:19,5:2,6:4,7:6,8:11,9:5,10:3,11:7,12:25,13:15,14:13,15:17,16:18,17:12,18:16,19:14,20:8}
firsts = [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,7),(0,8),(0,9),(0,10),(0,11),
          (1,1),(1,3),(1,4),(1,5),(1,7),(1,10),(2,1),(2,2),(2,4),(2,5)]
CW, CH = 50, 60
canvas = Image.new("RGB", (CW*3, len(firsts)*(CH+6)), (20,20,20))
dr = ImageDraw.Draw(canvas)
for gi,(r,c) in enumerate(firsts):
    y = gi*(CH+6)
    pet = mapping[gi]
    im = Image.open(f"assets/tiles/pet_{pet:02d}.png").convert("RGBA")
    bg = Image.new("RGBA", im.size, (255, 200, 225, 255))
    bg.alpha_composite(im)
    ref = bg.convert("RGB").resize((40, 52), Image.LANCZOS)
    cell = img.crop((xs[c]+3, ys[r]+3, xs[c]+37, ys[r]+47))
    dr.text((14, y+2), f"G{gi}", fill=(255,255,0))
    canvas.paste(cell, (4, y+10))
    canvas.paste(ref, (CW+4, y+10))
    dr.text((CW+18, y+2), f"#{pet}", fill=(0,255,0))
    # 差异标识
    import numpy as np
    a = np.array(cell.resize((40,52), Image.LANCZOS)).astype(float)
    b = np.array(ref).astype(float)
    err = ((a-b)**2).mean()
    dr.text((CW*2+8, y+2), f"{int(err)}", fill=(255,100,100))
canvas = canvas.resize((canvas.width*3, canvas.height*3), Image.NEAREST)
canvas.save("verify_final.png")
print("OUTPUT=" + __import__("os").path.abspath("verify_final.png"))
