# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw
cols, rows = 7, 6
CW, CH = 60, 66
canvas = Image.new("RGB", (cols*CW, rows*(CH+14)), (25,25,25))
dr = ImageDraw.Draw(canvas)
for i in range(42):
    im = Image.open(f"assets/tiles/pet_{i:02d}.png").convert("RGBA")
    bg = Image.new("RGBA", im.size, (255, 200, 225, 255))
    bg.alpha_composite(im)
    im = bg.convert("RGB").resize((48, 60), Image.NEAREST)
    r, c = i // cols, i % cols
    canvas.paste(im, (c*CW+6, r*(CH+14)+12))
    dr.text((c*CW+26, r*(CH+14)), str(i), fill=(255,255,0))
canvas = canvas.resize((canvas.width*2, canvas.height*2), Image.NEAREST)
canvas.save("ref_all.png")
print("OUTPUT=" + __import__("os").path.abspath("ref_all.png"))
