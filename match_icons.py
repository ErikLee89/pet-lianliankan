# -*- coding: utf-8 -*-
# 从原版游戏截图中识别棋盘每个格子用的是哪个图标
import numpy as np
from PIL import Image

SHOT = r"C:\Users\Erik\AppData\Local\Temp\comate_app_clipboard\image_aa60d7aa.png"
img = np.array(Image.open(SHOT).convert("RGB")).astype(int)
H, W = img.shape[:2]
R, G, B = img[:,:,0], img[:,:,1], img[:,:,2]

# 1) 找粉色棋盘区域（原版牌面底色是粉/品红）
pink = (R > 200) & (B > 140) & (G < R - 40) & (G < 200)
ys, xs = np.where(pink)
print(f"截图尺寸: {W}x{H}, 粉色像素: {len(xs)}")
x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
print(f"棋盘包围盒: x[{x0},{x1}] y[{y0},{y1}]  宽{x1-x0+1} 高{y1-y0+1}")
tw = (x1 - x0 + 1) / 12.0
th = (y1 - y0 + 1) / 8.0
print(f"每格约: {tw:.1f} x {th:.1f} px")

# 2) 加载42张参考图（透明PNG，贴到粉色底上模拟原版效果）
refs = []
for i in range(42):
    im = Image.open(f"assets/tiles/pet_{i:02d}.png").convert("RGBA")
    bg = Image.new("RGBA", im.size, (255, 190, 220, 255))
    bg.alpha_composite(im)
    refs.append(np.array(bg.convert("RGB")).astype(int))

def cell_crop(cx, cy, w, h, pad=3):
    return img[cy+pad:cy+h-pad, cx+pad:cx+w-pad]

# 3) 逐格比对
from collections import Counter
used = Counter()
grid_ids = []
for r in range(8):
    row = []
    for c in range(12):
        cx, cy = int(x0 + c*tw), int(y0 + r*th)
        cw, ch = int(tw), int(th)
        cell = cell_crop(cx, cy, cw, ch)
        cell_img = Image.fromarray(cell.astype(np.uint8)).resize((33, 33), Image.LANCZOS)
        cell = np.array(cell_img).astype(int)
        best, bestd = -1, 1e18
        for i, ref in enumerate(refs):
            ref_r = np.array(Image.fromarray(ref.astype(np.uint8)).resize((33,33), Image.LANCZOS)).astype(int)
            d = ((cell - ref_r) ** 2).mean()
            if d < bestd:
                bestd, best = d, i
        row.append(best)
        used[best] += 1
    grid_ids.append(row)

print("\n识别出的棋盘（每格为图标编号）:")
for row in grid_ids:
    print(" ".join(f"{v:2d}" for v in row))

ids = sorted(used)
print(f"\n不同图标数: {len(ids)}")
print("图标清单:", ids)
print("各图标出现次数:", dict(sorted(used.items())))
