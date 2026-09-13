# -*- coding: utf-8 -*-
# 模拟第4关左右分离位移，验证只补空洞不拉散
COLS=12; ROWS=8; MID=COLS//2
def simulate(row, holes):
    # row: 长度12的列表，1=有牌 0=空。holes: 要置空的列索引集合(0-based, 对应x=1..12)
    r=row[:]
    for h in holes: r[h]=0
    # 模拟 while 循环的位移
    moved=True; g=0
    while moved and g<200:
        moved=False; g+=1
        # 左半区(x=1..6 即索引0..5)向左滑：空洞x由x+1补
        for x in range(0, MID):  # 索引0..5
            if r[x]==0 and x+1<=MID-1 and r[x+1]==1:  # x+1<=MID-1 即不越过中线(中线在索引5和6之间)
                r[x]=r[x+1]; r[x+1]=0; moved=True
        # 右半区(x=7..12 即索引6..11)向右滑：空洞x由x-1补
        for x in range(COLS-1, MID-1, -1):  # 索引11..6
            if r[x]==0 and x-1>=MID and r[x-1]==1:
                r[x]=r[x-1]; r[x-1]=0; moved=True
    return r

full=[1]*12
print("满盘消除中间一对(列6,7即索引5,6):")
res=simulate(full,{5,6})
print(" 结果:", "".join(str(v) for v in res))
print(" 左半区牌数:",sum(res[:6]),"右半区牌数:",sum(res[6:]))

print("\n满盘消除最左边一对(索引0,1):")
res=simulate(full,{0,1})
print(" 结果:", "".join(str(v) for v in res))

print("\n满盘消除分散两对(索引2,3 和 8,9):")
res=simulate(full,{2,3,8,9})
print(" 结果:", "".join(str(v) for v in res))

print("\n验证不越过中线：左半区消除后左半区牌应=原左半区牌-消除数")
