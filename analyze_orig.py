# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np, os
# 读你最初的原版截图
src = r"C:\Users\Erik\AppData\Local\Temp\comate_app_clipboard\image_aa60d7aa.png"
img = Image.open(src).convert("RGB")
W,H = img.size
print("原版截图尺寸:", img.size)
# 裁剪棋盘区域放大（先全图缩放到能看清）
img2 = img.resize((W*1, H*1), Image.NEAREST)
img2.save("orig_full.png")
print("OUTPUT="+os.path.abspath("orig_full.png"))
