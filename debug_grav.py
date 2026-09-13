# -*- coding: utf-8 -*-
# 精确复刻第4关 sep:"h" 的位移逻辑，验证满盘消除后是否移动
COLS=12; ROWS=8
def emptyGrid():
    return [[-1]*(COLS+2) for _ in range(ROWS+2)]

grid=emptyGrid()
# 满盘：x=1..12, y=1..8
n=0
for y in range(1,ROWS+1):
    for x in range(1,COLS+1):
        grid[y][x]=n; n+=1

# 模拟消除一对：第4行(y=4)的 x=5 和 x=6（左半区）
grid[4][5]=-1; grid[4][6]=-1

MID=COLS//2
def move(x,y,nx,ny):
    if nx<1 or nx>COLS or ny<1 or ny>ROWS: return False
    if grid[ny][nx]>=0: return False
    grid[ny][nx]=grid[y][x]; grid[y][x]=-1
    return True

moved=True; guard=0; total_moves=0
while moved and guard<200:
    moved=False; guard+=1
    # sep:"h" 逻辑（照抄JS）
    for y in range(1,ROWS+1):
        for x in range(1,MID+1):
            if grid[y][x]<0 and x+1<=COLS+1 and grid[y][x+1] is not None and grid[y][x+1]>=0 and x+1<=MID:
                if move(x+1,y,x,y): moved=True; total_moves+=1
        for x in range(COLS,MID,-1):
            if grid[y][x]<0 and x-1>=1 and grid[y][x-1] is not None and grid[y][x-1]>=0 and x-1>=MID+1:
                if move(x-1,y,x,y): moved=True; total_moves+=1

print("总移动次数:",total_moves)
# 打印消除那一行(y=4)的最终状态（显示每列的牌编号或空）
row4=[grid[4][x] for x in range(1,COLS+1)]
print("第4行最终:",["空" if v<0 else v for v in row4])
