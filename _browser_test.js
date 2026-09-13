// 在游戏页面加载后注入执行，验证第4关分离
(function(){
  const out=[];
  try{
    const COLS=12,ROWS=8;
    // 强制设为第4关并重建棋盘
    level=4;
    buildBoard && null;
    // buildBoard 是内部的，直接构造满盘
    grid=[];for(let y=0;y<ROWS+2;y++)grid.push(new Array(COLS+2).fill(-1));
    tiles=new Map();
    let n=0;
    for(let y=1;y<=ROWS;y++)for(let x=1;x<=COLS;x++){
      grid[y][x]=n%21;n++;
      const el=document.createElement("div");el.className="tile";
      el.style.position="absolute";
      el.dataset.x=x;el.dataset.y=y;
      tiles.set(x+","+y,el);
    }
    const before=JSON.stringify(grid[4].slice(1,13));
    // 消除一对：左半区相邻 x=5,6
    grid[4][5]=-1;grid[4][6]=-1;tiles.delete("5,4");tiles.delete("6,4");
    applyGravity();
    const after=JSON.stringify(grid[4].slice(1,13));
    out.push("第4关消除左半区相邻x5,x6:");
    out.push("  前:"+before);
    out.push("  后:"+after);
    out.push(before!==after?"  ✅有移动":"  ❌没动");
    // 第5关测试
    level=5;
    grid=[];for(let y=0;y<ROWS+2;y++)grid.push(new Array(COLS+2).fill(-1));
    tiles=new Map();n=0;
    for(let y=1;y<=ROWS;y++)for(let x=1;x<=COLS;x++){grid[y][x]=n%21;n++;const el=document.createElement("div");el.dataset.x=x;el.dataset.y=y;tiles.set(x+","+y,el);}
    const b5=JSON.stringify(grid.map(r=>r[6]));  // 看第6列
    grid[3][6]=-1;grid[4][6]=-1;tiles.delete("6,3");tiles.delete("6,4"); // 消除上半区相邻
    applyGravity();
    const a5=JSON.stringify(grid.map(r=>r[6]));
    out.push("第5关消除上半区相邻y3,y4(第6列):");
    out.push("  前:"+b5);out.push("  后:"+a5);
    out.push(b5!==a5?"  ✅有移动":"  ❌没动");
  }catch(e){out.push("错误:"+e.message+" "+e.stack);}
  document.title="TEST::"+out.join("\n");
  // 也写到 body
  const d=document.createElement("pre");d.id="testout";d.textContent=out.join("\n");document.body.appendChild(d);
})();
