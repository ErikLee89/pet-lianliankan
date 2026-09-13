# -*- coding: utf-8 -*-
# 这几个图透明通道提取有问题，尝试不同的透明处理方式
from PIL import Image, ImageDraw
import numpy as np
ids = [0, 3, 10, 13, 15, 17, 25]
CW, CH = 80, 90
canvas = Image.new("RGB", (len(ids)*CW, (CH+16)*2), (20,20,20))
dr = ImageDraw.Draw(canvas)
for k, i in enumerate(ids):
    im = Image.open(f"assets/tiles/pet_{i:02d}.png")
    # 方式1：alpha合成到粉底
    bg1 = Image.new("RGBA", im.size, (255,200,225,255))
    bg1.alpha_composite(im.convert("RGBA"))
    # 方式2：直接用RGB通道（忽略alpha）
    rgb = im.convert("RGB")
    # 方式3：把纯黑(0,0,0)替换为粉色，其余保留
    arr = np.array(rgb)
    mask = (arr.sum(axis=2) < 30)
    arr[mask] = [255, 200, 225]
    fix = Image.fromarray(arr)
    canvas.paste(bg1.convert("RGB").resize((60,76), Image.NEAREST), (k*CW+10, 14))
    dr.text((k*CW+34, 0), str(i), fill=(255,255,0))
    canvas.paste(fix.resize((60,76), Image.NEAREST), (k*CW+10, CH+30))
canvas = canvas.resize((canvas.width*2, canvas.height*2), Image.NEAREST)
canvas.save("check_transparent.png")
print("OUTPUT=" + __import__("os").path.abspath("check_transparent.png"))
