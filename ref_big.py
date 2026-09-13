# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw
# 放大显示 0,1,3,4,5,13,18,19,25,26,37,38 等易混淆参考图
ids = [0,1,3,4,5,6,7,8,9,11,12,13,14,16,18,19,20,25,26,35,37,38,40]
n = len(ids)
CW, CH = 44, 52
canvas = Image.new("RGB", (n*CW, CH), (20,20,20))
dr = ImageDraw.Draw(canvas)
for k, i in enumerate(ids):
    im = Image.open(f"assets/tiles/pet_{i:02d}.png").convert("RGBA")
    bg = Image.new("RGBA", im.size, (255, 200, 225, 255))
    bg.alpha_composite(im)
    im = bg.convert("RGB").resize((34, 44), Image.NEAREST)
    canvas.paste(im, (k*CW+5, 8))
    dr.text((k*CW+18, 0), str(i), fill=(255,255,0))
canvas = canvas.resize((canvas.width*4, canvas.height*4), Image.NEAREST)
canvas.save("ref_big.png")
print("OUTPUT=" + __import__("os").path.abspath("ref_big.png"))
