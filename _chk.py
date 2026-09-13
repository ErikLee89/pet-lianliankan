# -*- coding: utf-8 -*-
import re
html=open("index.html",encoding="utf-8").read()
js=re.search(r"<script>([\s\S]*?)</script>",html).group(1)
open("_g.js","w",encoding="utf-8").write(js)
# 打印 applyGravity 完整代码确认结构
m=re.search(r"function applyGravity\(\)\{([\s\S]*?)\n\}\n// ===== 状态",js)
print("=== applyGravity 结构 ===")
print(m.group(0)[:1500] if m else "未找到")
