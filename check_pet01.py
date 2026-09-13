# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw
import numpy as np
# 图集原始 #1（黑底）
sheet = Image.open("res/bmp_129.png").convert("RGB")
orig = sheet.crop((4*39, 1*39, 4*39+39, 1*39+39))
# 游戏里提取后的 pet_01（透明底，放粉/紫底看）
ext = Image.open("assets/tiles/pet_01.png").convert("RGBA")
bg = Image.new("RGBA", ext.size, (255,200,225,255))
bg.alpha_composite(ext)
ext_onbg = bg.convert("RGB")
# 并排放大
canvas=Image.new("RGB",(2*110+20, 130),(20,20,20))
dr=ImageDraw.Draw(canvas)
canvas.paste(orig.resize((100,100),Image.NEAREST),(5,25))
dr.text((20,5),"图集#1(原)",fill=(0,255,0))
canvas.paste(ext_onbg.resize((100,100),Image.NEAREST),(115,25))
dr.text((120,5),"提取后pet_01",fill=(255,150,0))
canvas.save("pet01_cmp.png")
print("OUTPUT="+__import__("os").path.abspath("pet01_cmp.png"))

# 分析原图#1的触角区域（顶部y0-8）有哪些像素，提取后是否保留
oa=np.array(orig).astype(int)
ea=np.array(ext.split()[3])  # alpha通道
print("\n原图#1 顶部y0-9 内容像素(>60)每行数:")
for y in range(10):
    print(f"  y{y}: 原图内容={(oa[y].sum(axis=1)>60).sum()}, 提取后alpha>0={(ea[y]>0).sum()}")
