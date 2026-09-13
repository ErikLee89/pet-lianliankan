// 用最小 DOM stub 加载游戏脚本，测试第4关左右分离
const fs=require('fs');
const html=fs.readFileSync('D:/test/lianliankan/index.html','utf8');
let js=html.match(/<script>([\s\S]*?)<\/script>/)[1];

// ===== 最小 DOM stub =====
const elements={};
function makeEl(tag){
  const el={
    tag, children:[], style:{}, dataset:{}, classList:{
      _s:new Set(),
      add(c){this._s.add(c)}, remove(c){this._s.delete(c)},
      toggle(c,f){f?this._s.add(c):this._s.delete(c)}, contains(c){return this._s.has(c)}
    },
    _html:'', set innerHTML(v){this._html=v; if(v==='')this.children=[];}, get innerHTML(){return this._html;},
    appendChild(c){this.children.push(c);return c;},
    addEventListener(){}, removeEventListener(){},
    querySelector(){return null;}, querySelectorAll(){return [];},
    getContext(){return {clearRect(){},beginPath(){},moveTo(){},lineTo(){},stroke(){},set strokeStyle(v){},set lineWidth(v){},set lineCap(v){},set lineJoin(v){},set shadowColor(v){},set shadowBlur(v){}};},
    set onclick(f){}, set oncontextmenu(f){},
    width:0,height:0
  };
  return el;
}
const byId={};
global.document={
  getElementById(id){ if(!byId[id])byId[id]=makeEl('div'); return byId[id];},
  createElement(t){return makeEl(t);},
  querySelectorAll(){return [];},
  addEventListener(){},
  body:makeEl('body')
};
global.window={};
global.localStorage={getItem(){return null;},setItem(){},};
global.Audio=function(){return {play(){},pause(){},cloneNode(){return {play(){}};},currentTime:0,volume:1,loop:false};};
global.requestAnimationFrame=()=>{};
global.Image=function(){return {set src(v){},onload:null};};

// 暴露内部函数：在脚本末尾追加
js+=`
;globalThis.__test={applyGravity,LAYOUTS,moveTileEl:(typeof moveTileEl!=='undefined'?moveTileEl:null)};
globalThis.__setState=(g,t,l)=>{grid=g;tiles=t;level=l;};
globalThis.__getGrid=()=>grid;
globalThis.__getTiles=()=>tiles;
`;
eval(js);

// ===== 构造第4关满盘 =====
const T=globalThis.__test;
const COLS=12,ROWS=8;
let grid=[];for(let y=0;y<ROWS+2;y++)grid.push(new Array(COLS+2).fill(-1));
let tiles=new Map();
let n=0;
for(let y=1;y<=ROWS;y++)for(let x=1;x<=COLS;x++){
  grid[y][x]=n%21; // 用21种牌循环
  const el=makeEl('div');el.dataset.x=x;el.dataset.y=y;
  tiles.set(x+","+y,el);
  n++;
}
// moveTileEl stub（游戏里的会操作 style）
global.moveTileEl=(x,y)=>{const el=tiles.get(x+","+y);if(el){el.style.left=x;el.style.top=y;}};
// 需要 moveTileEl 在 eval 作用域可见 —— 通过重新注入
globalThis.__setState(grid,tiles,4);

// 消除一对：y=4 行的 x=5 和 x=6（左半区相邻）
grid[4][5]=-1;grid[4][6]=-1;
tiles.delete("5,4");tiles.delete("6,4");

// 记录移动前 grid 第4行
const before=grid[4].slice(1,13).map(v=>v<0?'·':String(v).padStart(2,'0')).join(' ');
// 手动注入 moveTileEl 到 eval 的词法作用域不可行，改用替代：直接调用 applyGravity 内部用的 moveTileEl
// 由于 moveTileEl 在游戏脚本里是顶层函数，eval 后应已存在于 globalThis
try{
  T.applyGravity();
}catch(e){console.log("applyGravity 报错:",e.message);process.exit(1);}
const after=globalThis.__getGrid()[4].slice(1,13).map(v=>v<0?'·':String(v).padStart(2,'0')).join(' ');
console.log("第4关 左右分离 —— 第4行消除 x5,x6 后:");
console.log("  消除前:",before);
console.log("  位移后:",after);
const moved=before!==after;
console.log(moved?"  ✅ 有移动！":"  ❌ 仍然没动");
