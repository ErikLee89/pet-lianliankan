# -*- coding: utf-8 -*-
# 验证"向两边压实"的分离逻辑
COLS=12; ROWS=8; MID=COLS//2
def simulate(holes, y=4):
    grid=[[-1]*(COLS+2) for _ in range(ROWS+2)]
    n=0
    for yy in range(1,ROWS+1):
        for x in range(1,COLS+1):
            grid[yy][x]=n; n+=1
    for h in holes: grid[y][h]=-1
    # 左半区(x=1..6)压实：牌向左靠，空洞移到中线侧(x=6端)
    for yy in range(1,ROWS+1):
        # 收集左半区非空牌
        tiles=[grid[yy][x] for x in range(1,MID+1) if grid[yy][x]>=0]
        for i,x in enumerate(range(1,MID+1)):
            grid[yy][x]= tiles[i] if i<len(tiles) else -1
        # 右半区(x=7..12)压实：牌向右靠，空洞移到中线侧(x=7端)
        tiles=[grid[yy][x] for x in range(MID+1,COLS+1) if grid[yy][x]>=0]
        # 右半区从右往左填
        for i,x in enumerate(range(COLS,MID,-1)):
            idx=len(tiles)-1-i
            grid[yy][x]= tiles[idx] if idx>=0 else -1
    row=[grid[y][x] for x in range(1,COLS+1)]
    return ["空" if v<0 else v for v in row]

print("消除左半区相邻 x=5,6:")
print(" ", simulate([5,6]))
print("\n消除左半区单个 x=3:")
print(" ", simulate([3]))
print("\n消除右半区 x=8,9:")
print(" ", simulate([8,9]))
print("\n消除跨中线 x=6(左),7(右):")
print(" ", simulate([6,7]))
