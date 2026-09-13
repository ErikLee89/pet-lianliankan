# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw
CW, CH = 40, 50
cols = 14
rows = 3
canvas = Image.new("RGB", (cols*CW, rows*(CH+12)), (30,30,30))
dr = ImageDraw.Draw(canvas)
for i in range(42):
    im = Image.open(f"assets/tiles/pet_{i:02d}.png").convert("RGBA")
    bg = Image.new("RGBA", im.size, (255, 200, 225, 255))
    bg.alpha_composite(im)
    im = bg.convert("RGB").resize((34, 44), Image.NEAREST)
    r, c = i // cols, i % cols
    canvas.paste(im, (c*CW+3, r*(CH+12)+10))
    dr.text((c*CW+16, r*(CH+12)), str(i), fill=(255,255,0))
canvas = canvas.resize((canvas.width*2, canvas.height*2), Image.NEAREST)
canvas.save("ref_sheet.png")
print("OUTPUT=" + __import__("os").path.abspath("ref_sheet.png"))
