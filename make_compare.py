# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
sheet = Image.open("res/bmp_129.png").convert("RGB")
# 生成 c2 和 c4 各42张的对比图（左c2右c4），黑底
cols=7
rows=6
CW=46; CH=58
canvas=Image.new("RGB",(cols*CW*2+20, rows*CH+20),(20,20,20))
dr=ImageDraw.Draw(canvas)
for i in range(42):
    rr=i//cols; cc=i%cols
    # c2
    a=sheet.crop((2*39,i*39,2*39+39,i*39+39))
    canvas.paste(a.resize((42,42),Image.NEAREST),(cc*CW, rr*CH+12))
    dr.text((cc*CW+16,rr*CH),f"{i}",fill=(0,255,0))
    # c4
    b=sheet.crop((4*39,i*39,4*39+39,i*39+39))
    canvas.paste(b.resize((42,42),Image.NEAREST),(cols*CW+10+cc*CW, rr*CH+12))
    dr.text((cols*CW+10+cc*CW+16,rr*CH),f"{i}",fill=(255,150,0))
# 标注
dr.text((2,2),"c2(候选真图)",fill=(0,255,0))
dr.text((cols*CW+12,2),"c4(当前用)",fill=(255,150,0))
canvas=canvas.resize((canvas.width,canvas.height),Image.NEAREST)
canvas.save("compare_c2c4.png")
print("OUTPUT="+__import__("os").path.abspath("compare_c2c4.png"))
