# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw
sheet = Image.open("res/bmp_129.png").convert("RGB")
suspects=[1,4,23,26,27,31]
canvas=Image.new("RGB",(len(suspects)*90+10, 110),(20,20,20))
dr=ImageDraw.Draw(canvas)
for k,i in enumerate(suspects):
    cell=sheet.crop((4*39,i*39,4*39+39,i*39+39))
    big=cell.resize((80,80),Image.NEAREST)
    canvas.paste(big,(k*90+5,22))
    dr.text((k*90+38,4),f"#{i}",fill=(255,255,0))
canvas.save("zoom_suspects.png")
print("OUTPUT="+__import__("os").path.abspath("zoom_suspects.png"))
