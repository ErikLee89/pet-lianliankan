# -*- coding: utf-8 -*-
# 导出几个关键参考图的大图，确认它们到底是什么宝可梦
from PIL import Image, ImageDraw
ids = [1,3,4,7,10,11,12,13,15,17,20,24,25,30,33,35,36,37,40]
CW, CH = 70, 80
cols = 5
rows = (len(ids)+cols-1)//cols
canvas = Image.new("RGB", (cols*CW, rows*(CH+16)), (25,25,25))
dr = ImageDraw.Draw(canvas)
for k, i in enumerate(ids):
    im = Image.open(f"assets/tiles/pet_{i:02d}.png").convert("RGBA")
    bg = Image.new("RGBA", im.size, (255, 200, 225, 255))
    bg.alpha_composite(im)
    im = bg.convert("RGB").resize((56, 70), Image.NEAREST)
    r, c = k // cols, k % cols
    canvas.paste(im, (c*CW+7, r*(CH+16)+14))
    dr.text((c*CW+30, r*(CH+16)), str(i), fill=(255,255,0))
canvas = canvas.resize((canvas.width*2, canvas.height*2), Image.NEAREST)
canvas.save("check_ref.png")
print("OUTPUT=" + __import__("os").path.abspath("check_ref.png"))
