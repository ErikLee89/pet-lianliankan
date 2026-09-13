# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw
sheet = Image.open("res/bmp_129.png").convert("RGB")
# 导出图集第32-35行、所有6列的格子，看瓢虫到底在哪列、是否完整
rows=[31,32,33,34]
CW=48
canvas=Image.new("RGB",(6*CW+10, len(rows)*CW+24),(40,40,40))
dr=ImageDraw.Draw(canvas)
for ri,r in enumerate(rows):
    for c in range(6):
        cell=sheet.crop((c*39,r*39,c*39+39,r*39+39))
        canvas.paste(cell.resize((44,44),Image.NEAREST),(c*CW+8, ri*CW+20))
        dr.text((c*CW+20, ri*CW+8), f"c{c}", fill=(255,255,0))
    dr.text((2, ri*CW+30), f"r{r}", fill=(0,255,255))
canvas=canvas.resize((canvas.width*2,canvas.height*2),Image.NEAREST)
canvas.save("cmp_cols.png")
print("OUTPUT="+__import__("os").path.abspath("cmp_cols.png"))

# 同时导出当前游戏里的 pet_31/32/33/34 对比
canvas2=Image.new("RGB",(4*60+10, 70),(40,40,40))
dr2=ImageDraw.Draw(canvas2)
for k,i in enumerate([31,32,33,34]):
    im=Image.open(f"assets/tiles/pet_{i:02d}.png").convert("RGBA")
    bg=Image.new("RGBA",im.size,(255,200,225,255))
    bg.alpha_composite(im)
    canvas2.paste(bg.convert("RGB").resize((50,50),Image.NEAREST),(k*60+8,14))
    dr2.text((k*60+24,0),f"p{i}",fill=(255,255,0))
canvas2=canvas2.resize((canvas2.width*2,canvas2.height*2),Image.NEAREST)
canvas2.save("cmp_pet_now.png")
print("OUTPUT="+__import__("os").path.abspath("cmp_pet_now.png"))
