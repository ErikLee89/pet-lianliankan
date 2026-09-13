# -*- coding: utf-8 -*-
import numpy as np
from PIL import Image
SHOT = r"C:\Users\Erik\AppData\Local\Temp\comate_app_clipboard\image_aa60d7aa.png"
img = Image.open(SHOT).convert("RGB")
xs = [162 + 40*c for c in range(12)]
ys = [160 + 50*r for r in range(8)]
refs = []
for i in range(42):
    im = Image.open(f"assets/tiles/pet_{i:02d}.png").convert("RGBA")
    bg = Image.new("RGBA", im.size, (255, 200, 225, 255))
    bg.alpha_composite(im)
    refs.append(bg.convert("RGB").resize((34, 44), Image.LANCZOS))
ref_arr = [np.array(r).astype(float) for r in refs]

# 先识别全棋盘，统计出现次数，凑不成偶数的就是误识别
def identify():
    board = []
    for r in range(8):
        row = []
        for c in range(12):
            a = np.array(img.crop((xs[c]+3, ys[r]+3, xs[c]+37, ys[r]+47))).astype(float)
            d = [((a - ra)**2).mean() for ra in ref_arr]
            row.append((int(np.argmin(d)), float(min(d))))
        board.append(row)
    return board

board = identify()
# 第8行是空白区，整行剔除
from collections import Counter
cnt = Counter()
for r in range(7):
    for c in range(12):
        v, d = board[r][c]
        if d < 15000: cnt[v] += 1
odd = {v: n for v, n in cnt.items() if n % 2 != 0}
print("出现奇数次的可疑图案:", odd)

# 对可疑格重新比对：排除掉凑成偶数的“确定图案”后重选
sure = {v for v, n in cnt.items() if n % 2 == 0}
final = {}
for r in range(7):
    for c in range(12):
        a = np.array(img.crop((xs[c]+3, ys[r]+3, xs[c]+37, ys[r]+47))).astype(float)
        d = [((a - ra)**2).mean() for ra in ref_arr]
        order = np.argsort(d)
        # 跳过所有sure图案之外的也要重新看
        for idx in order:
            if d[idx] < 15000:
                final[(r, c)] = int(idx)
                break
cnt2 = Counter(final.values())
print("\n修正后各图案次数:", dict(sorted(cnt2.items())))
ids = sorted(v for v in cnt2 if cnt2[v] % 2 == 0)
print("最终清单(偶数次):", ids, "共", len(ids), "种")
# 校验96 = 7行×12=84格 + 其余被识别? 84格/4 = 21种才对
print("已识别格数:", sum(cnt2.values()), "/ 84")
