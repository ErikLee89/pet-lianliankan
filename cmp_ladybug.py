# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np
sheet = Image.open("res/bmp_129.png").convert("RGB")  # 234x1638, 6列x42行
# 当前42张 pet 图
pets = [Image.open(f"assets/tiles/pet_{i:02d}.png").convert("RGBA") for i in range(42)]

# 把 pet 的 alpha 合成到黑底，与图集（黑底）比较
def to_black(im):
    bg = Image.new("RGBA", im.size, (0,0,0,255))
    bg.alpha_composite(im)
    return np.array(bg.convert("RGB")).astype(float)

# 对每个 pet，找它在图集中最匹配的格子位置
COLS=6
for pi in [34*6//6]:  # 占位
    pass

# 先确认：瓢虫在图集[34][2]，序号若按"列优先"则不同
# 我们直接把每个pet和图集所有252格比一遍，找最佳匹配位置
best_map={}
for pi,pet in enumerate(pets):
    pb = to_black(pet)
    best=None
    for r in range(42):
        for c in range(COLS):
            cell=np.array(sheet.crop((c*39,r*39,c*39+39,r*39+39))).astype(float)
            d=((pb-cell)**2).mean()
            if best is None or d<best[0]:
                best=(d,r,c)
    best_map[pi]=best
# 输出红色最多（瓢虫候选）的pet
reds=[]
for pi,pet in enumerate(pets):
    arr=np.array(pet.convert("RGB")).astype(int)
    a=np.array(pet.split()[3])
    red=((arr[:,:,0]>150)&(arr[:,:,1]<90)&(arr[:,:,2]<90)&(a>128)).sum()
    reds.append((red,pi))
reds.sort(reverse=True)
print("当前42张中红色最多的pet编号:")
for red,pi in reds[:4]:
    d,r,c=best_map[pi]
    print(f"  pet_{pi:02d} 红像素={red}  最匹配图集格[{r}][{c}] 误差={d:.0f}")
