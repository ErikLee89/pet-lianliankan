
"use strict";
const COLS=12, ROWS=8, TILE=56, MAX_LEVEL=10, KIND_COUNT=42;
const DIFF=[
 {name:"初级",time:220,bonus:10},
 {name:"中级",time:170,bonus:20},
 {name:"高级",time:130,bonus:30},
 {name:"特级",time:95, bonus:40}];
const LAYOUTS=[
 {name:"固定不动",dx:0,dy:0},{name:"向下移动",dx:0,dy:1},{name:"向左移动",dx:-1,dy:0},
 {name:"左右分离",sep:"h"},{name:"上下分离",sep:"v"},{name:"向右移动",dx:1,dy:0},
 {name:"向中集中",dx:0,dy:0,pushIn:true},{name:"上下向中",sep:"vIn"}];
const SFX={select:"select",match:"match",error:"error",hint:"hint",tick:"tick",shuffle:"shuffle",levelstart:"levelstart",win:"win",gameover:"gameover"};
const TIME_BONUS=2; // 每消除一对奖励的秒数
const boardEl=document.getElementById("board"),fx=document.getElementById("fx"),fctx=fx.getContext("2d");
const $=id=>document.getElementById(id);
let grid=[],tiles=new Map(),sel=null,hintPair=null;
let level=1,diff=0,score=0,lives=3,hints=3,remain=0,timer=null,paused=false,over=false,soundOn=true;
let startLevel=1; // 起始关卡（测试用，可从菜单选）
let tileSet=localStorage.getItem("llk_tileset")||"pet";
$("setSel").value=tileSet;
// ===== 资源预加载 =====
const IMG={pet:[],jp:[],sign:[]};
(function(){
 for(const s of["pet","jp","sign"])for(let i=0;i<KIND_COUNT;i++){const im=new Image();im.src=`assets/tiles/${s}_${String(i).padStart(2,"0")}.png`;IMG[s].push(im);}
})();
const AUDIO={};
for(const k in SFX){const a=new Audio(`assets/sfx/${SFX[k]}.wav`);a.preload="auto";AUDIO[k]=a;}
function play(k){if(!soundOn)return;const a=AUDIO[k];if(!a)return;try{a.currentTime=0;a.play().catch(()=>{});}catch(e){}}
// ===== 牌面 =====
function drawTile(el,kind){
 el.innerHTML="";
 const im=document.createElement("img");
 im.src=IMG[tileSet][kind].src;
 el.appendChild(im);
}
// ===== 工具 =====
function shuffled(a){for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;}
function toast(m){const t=$("toast");t.textContent=m;t.style.opacity=1;setTimeout(()=>t.style.opacity=0,1600);}
// ===== 棋盘生成 =====
function emptyGrid(){return Array.from({length:ROWS+2},()=>Array(COLS+2).fill(-1));}
function fillPositions(){
 const L=LAYOUTS[(level-1)%LAYOUTS.length];const pts=[];
 // 所有牌型都在真实8×12棋盘上生成，保证坐标合法；分离效果靠消除后的重力位移呈现
 for(let y=1;y<=ROWS;y++)for(let x=1;x<=COLS;x++)pts.push([x,y]);
 return pts;
}
// 按难度限制图案种类（原程序：简单模式只用部分图案）
// 初级21种 / 中级28种 / 高级35种 / 特级42种
const POOL_SIZES=[21,28,35,42];
function kinds48(){
 const pool=POOL_SIZES[diff]||21;
 const order=shuffled([...Array(pool).keys()]);
 const ks=[];for(let i=0;i<COLS*ROWS/2;i++)ks.push(order[i%pool]);
 return ks;
}
function setupCanvas(){
 boardEl.style.width=COLS*TILE+"px";
 boardEl.style.height=ROWS*TILE+"px";
 // canvas 比棋盘大一圈（四周各留 TILE），以容纳绕外圈的连线
 fx.width=(COLS+2)*TILE;fx.height=(ROWS+2)*TILE;
 fx.style.width=(COLS+2)*TILE+"px";fx.style.height=(ROWS+2)*TILE+"px";
}
function buildBoard(){ // 根据当前 level 铺牌（牌型由 level 决定）
 grid=emptyGrid();
 const kinds=kinds48(),deck=shuffled(kinds.concat(kinds)),pts=fillPositions();
 pts.forEach((p,i)=>grid[p[1]][p[0]]=deck[i]);
 remain=levelTime();sel=null;
 renderAll();updUI();
}
function newGame(){
 setupCanvas();
 level=startLevel;lives=3;hints=3;score=0;over=false;paused=false;
 $("pauseMask").style.display="none";
 buildBoard();startTimer();play("levelstart");
}
function levelTime(){return DIFF[diff].time;}
function nextLevel(){
 level++;
 if(level>MAX_LEVEL){winGame();return;}
 buildBoard();play("levelstart");
}
// ===== 渲染 =====
function renderAll(){
 tiles.forEach(el=>el.remove());tiles.clear();
 for(let y=1;y<=ROWS;y++)for(let x=1;x<=COLS;x++){
  const k=grid[y][x];if(k<0)continue;
  const el=document.createElement("div");el.className="tile";
  el.dataset.x=x;el.dataset.y=y;
  el.style.left=(x-1)*TILE+"px";el.style.top=(y-1)*TILE+"px";
  drawTile(el,k);
  el.onclick=()=>onTile(+el.dataset.x,+el.dataset.y); // 读取位移后的当前坐标
  el.oncontextmenu=e=>{e.preventDefault();onRightClick();};
  boardEl.appendChild(el);tiles.set(x+","+y,el);
 }
}
function moveTileEl(x,y){
 const t=tiles.get(x+","+y);if(!t)return;
 t.dataset.x=x;t.dataset.y=y; // 同步当前坐标，点击时才能取到正确值
 t.style.left=(x-1)*TILE+"px";t.style.top=(y-1)*TILE+"px";
}
// ===== 连通性（核心逻辑）=====
function cellFree(x,y,ax,ay,bx,by){
 if(x<0||x>COLS+1||y<0||y>ROWS+1)return false;
 if((x===ax&&y===ay)||(x===bx&&y===by))return true;
 return grid[y][x]<0;
}
function canLink(ax,ay,bx,by){
 const g=grid;
 if(g[ay][ax]<0||g[by][bx]<0||g[ay][ax]!==g[by][bx])return null;
 const ok=(x,y)=>cellFree(x,y,ax,ay,bx,by);
 if(ax===bx){let clear=true;for(let y=Math.min(ay,by)+1;y<Math.max(ay,by);y++)if(!ok(ax,y)){clear=false;break;}
  if(clear)return[[ax,ay],[bx,by]];}
 if(ay===by){let clear=true;for(let x=Math.min(ax,bx)+1;x<Math.max(ax,bx);x++)if(!ok(x,ay)){clear=false;break;}
  if(clear)return[[ax,ay],[bx,by]];}
 if(ok(ax,by)&&segV(ax,ay,by,ok)&&segH(by,ax,bx,ok))return[[ax,ay],[ax,by],[bx,by]];
 if(ok(bx,ay)&&segH(ay,ax,bx,ok)&&segV(bx,ay,by,ok))return[[ax,ay],[bx,ay],[bx,by]];
 for(let y=0;y<=ROWS+1;y++){
  if(!ok(ax,y)||!ok(bx,y))continue;
  if(segV(ax,ay,y,ok)&&segH(y,ax,bx,ok)&&segV(bx,by,y,ok))
   return[[ax,ay],[ax,y],[bx,y],[bx,by]];
 }
 for(let x=0;x<=COLS+1;x++){
  if(!ok(x,ay)||!ok(x,by))continue;
  if(segH(ay,ax,x,ok)&&segV(x,ay,by,ok)&&segH(by,x,bx,ok))
   return[[ax,ay],[x,ay],[x,by],[bx,by]];
 }
 return null;
}
function segV(x,y1,y2,ok){if(y1===y2)return true;for(let y=Math.min(y1,y2)+1;y<Math.max(y1,y2);y++)if(!ok(x,y))return false;return true;}
function segH(y,x1,x2,ok){if(x1===x2)return true;for(let x=Math.min(x1,x2)+1;x<Math.max(x1,x2);x++)if(!ok(x,y))return false;return true;}
function findHint(){
 for(let y1=1;y1<=ROWS;y1++)for(let x1=1;x1<=COLS;x1++){
  if(grid[y1][x1]<0)continue;
  for(let y2=y1;y2<=ROWS;y2++){
   const xs=(y2===y1)?x1+1:1;
   for(let x2=xs;x2<=COLS;x2++){
    if(grid[y2][x2]<0)continue;
    const path=canLink(x1,y1,x2,y2);
    if(path)return{a:[x1,y1],b:[x2,y2],path};
   }
  }
 }
 return null;
}
// ===== 点击 =====
// 右键：取消当前点选
function onRightClick(){
 if(paused||over)return;
 if(sel){const t=tiles.get(sel[0]+","+sel[1]);if(t)t.classList.remove("sel");sel=null;play("select");}
 clearHintFlash();
}
function onTile(x,y){
 if(paused||over)return;
 const k=grid[y][x];if(k<0)return;
 clearHintFlash();
 if(!sel){sel=[x,y];tiles.get(x+","+y).classList.add("sel");play("select");return;}
 if(sel[0]===x&&sel[1]===y){tiles.get(x+","+y).classList.remove("sel");sel=null;return;}
 const path=canLink(sel[0],sel[1],x,y);
 if(path){
  // 先画连线并保留牌，停留后再消除，让用户看到连线过程
  drawPath(path,"#ff4040");play("match");
  const t1=tiles.get(sel[0]+","+sel[1]),t2=tiles.get(x+","+y);
  // 两张牌同步高亮
  if(t1)t1.classList.add("sel");
  if(t2)t2.classList.add("sel");
  const ax=sel[0],ay=sel[1];
  grid[ay][ax]=-1;grid[y][x]=-1;
  tiles.delete(ax+","+ay);tiles.delete(x+","+y);
  sel=null;
  setTimeout(()=>{fctx.clearRect(0,0,fx.width,fx.height);t1.remove();t2.remove();applyGravity();
   score+=2;
   // 每消除一对奖励时间，封顶不超过本关总时间
   remain=Math.min(levelTime(),remain+TIME_BONUS);
   updUI();checkState();},180);
 }else{
  tiles.get(sel[0]+","+sel[1]).classList.remove("sel");
  if(grid[y][x]===grid[sel[1]][sel[0]])play("error");
  sel=[x,y];tiles.get(x+","+y).classList.add("sel");play("select");
 }
}
function drawPath(path,color){
 fctx.clearRect(0,0,fx.width,fx.height);
 fctx.strokeStyle=color;fctx.lineWidth=3;fctx.lineCap="round";fctx.lineJoin="round";
 fctx.shadowColor=color;fctx.shadowBlur=6;
 fctx.beginPath();
 // 网格坐标 + TILE 偏移（因为 canvas 向左上扩了一圈）
 path.forEach((p,i)=>{const px=p[0]*TILE+TILE/2,py=p[1]*TILE+TILE/2;i?fctx.lineTo(px,py):fctx.moveTo(px,py);});
 fctx.stroke();
 fctx.shadowBlur=0;
}
// ===== 牌型位移 =====
// 压实一行：把 y 行 [x1,x2] 区间内的牌向 rev?右:左 边界压实，保持相对顺序，空洞移到另一端。同步更新 grid、tiles、DOM
function compactRow(y,x1,x2,rev){
 const xs=[];for(let x=x1;x<=x2;x++)xs.push(x);
 // 收集区间内的 {val, el}（按 x 升序，保持相对顺序）
 const items=[];
 for(const x of xs){
  const el=tiles.get(x+","+y);
  if(el&&grid[y][x]>=0)items.push({val:grid[y][x],el});
  tiles.delete(x+","+y);grid[y][x]=-1;
 }
 // 目标填充顺序：左靠从 x1 向右填，右靠从 x2 向左填
 const fillOrder=rev?xs.slice().reverse():xs;
 const fillItems=rev?items.slice().reverse():items;
 fillOrder.forEach((x,i)=>{
  const it=fillItems[i];if(!it)return;
  grid[y][x]=it.val;
  tiles.set(x+","+y,it.el);
  it.el.dataset.x=x;it.el.dataset.y=y;
  moveTileEl(x,y);
 });
}
// 压实一列：把 x 列 [y1,y2] 区间内的牌向 rev?下:上 边界压实
function compactCol(x,y1,y2,rev){
 const ys=[];for(let y=y1;y<=y2;y++)ys.push(y);
 const items=[];
 for(const y of ys){
  const el=tiles.get(x+","+y);
  if(el&&grid[y][x]>=0)items.push({val:grid[y][x],el});
  tiles.delete(x+","+y);grid[y][x]=-1;
 }
 const fillOrder=rev?ys.slice().reverse():ys;
 const fillItems=rev?items.slice().reverse():items;
 fillOrder.forEach((y,i)=>{
  const it=fillItems[i];if(!it)return;
  grid[y][x]=it.val;tiles.set(x+","+y,it.el);it.el.dataset.x=x;it.el.dataset.y=y;moveTileEl(x,y);
 });
}
function applyGravity(){
 const L=LAYOUTS[(level-1)%LAYOUTS.length];
 const move=(x,y,nx,ny)=>{
  if(nx<1||nx>COLS||ny<1||ny>ROWS)return false;
  if(grid[ny][nx]>=0)return false;
  grid[ny][nx]=grid[y][x];grid[y][x]=-1;
  const el=tiles.get(x+","+y);tiles.delete(x+","+y);tiles.set(nx+","+ny,el);
  moveTileEl(nx,ny);return true;
 };
 // ===== 分离/压实类牌型：一次性压实，直接返回 =====
 if(L.sep==="h"){ // 左右分离：左右两区各自向两侧边界压实，空洞移到中线侧
  const MID=COLS/2;
  for(let y=1;y<=ROWS;y++){compactRow(y,1,MID,false);compactRow(y,MID+1,COLS,true);}
  return;
 }
 if(L.sep==="v"){ // 上下分离：上下两区各自向上下边界压实，空洞移到中线
  const MH=ROWS/2;
  for(let x=1;x<=COLS;x++){compactCol(x,1,MH,false);compactCol(x,MH+1,ROWS,true);}
  return;
 }
 if(L.sep==="vIn"){ // 上下向中：上半区向下、下半区向上压实，空洞移到上下边界
  const MH=ROWS/2;
  for(let x=1;x<=COLS;x++){compactCol(x,1,MH,true);compactCol(x,MH+1,ROWS,false);}
  return;
 }
 // ===== 平移/向中类牌型：逐格位移，循环直至稳定 =====
 let moved=true,guard=0;
 while(moved&&guard++<200){
  moved=false;
  if(L.dx!==0||L.dy!==0){
   const xs=[],ys=[];
   for(let y=1;y<=ROWS;y++)for(let x=1;x<=COLS;x++)if(grid[y][x]>=0){xs.push(x);ys.push(y);}
   const order=xs.map((x,i)=>[x,ys[i]]);
   if(L.dx>0)order.sort((a,b)=>b[0]-a[0]);
   if(L.dx<0)order.sort((a,b)=>a[0]-b[0]);
   if(L.dy>0)order.sort((a,b)=>b[1]-a[1]);
   if(L.dy<0)order.sort((a,b)=>a[1]-b[1]);
   for(const[x,y]of order)if(grid[y]&&grid[y][x]>=0&&move(x,y,x+L.dx,y+L.dy))moved=true;
  }
  if(L.pushIn){
   for(let y=1;y<=ROWS;y++){
    for(let x=1;x<=6;x++)if(grid[y][x]>=0&&grid[y][x+1]<0){move(x,y,x+1,y);moved=true;}
    for(let x=COLS;x>=7;x--)if(grid[y][x]>=0&&grid[y][x-1]<0){move(x,y,x-1,y);moved=true;}
   }
   for(let x=1;x<=COLS;x++){
    for(let y=1;y<=3;y++)if(grid[y][x]>=0&&grid[y+1][x]<0){move(x,y,x,y+1);moved=true;}
    for(let y=ROWS;y>=6;y--)if(grid[y][x]>=0&&grid[y-1][x]<0){move(x,y,x,y-1);moved=true;}
   }
   for(let y=1;y<=4;y++)for(let x=1;x<=COLS;x++)if(grid[y][x]>=0&&grid[y+1]&&grid[y+1][x]<0&&y+1<=4){move(x,y,x,y+1);moved=true;}
   for(let y=ROWS;y>=5;y--)for(let x=1;x<=COLS;x++)if(grid[y][x]>=0&&grid[y-1]&&grid[y-1][x]<0&&y-1>=5){move(x,y,x,y-1);moved=true;}
  }
 }
}
// ===== 状态 =====
function tilesLeft(){let n=0;for(let y=1;y<=ROWS;y++)for(let x=1;x<=COLS;x++)if(grid[y][x]>=0)n++;return n;}
function checkState(){
 if(tilesLeft()===0){
  score+=remain+DIFF[diff].bonus;updUI();play("win");
  setTimeout(()=>{toast(`过关！时间奖励已计入，进入第 ${level+1>MAX_LEVEL?"—":level+1} 关`);nextLevel();},600);
  return;
 }
 if(!findHint())autoShuffle();
}
function autoShuffle(){
 if(lives>1){lives--;reshuffle(false);toast("死局！自动重排，生命 -1");updUI();}
 else gameOver("无可消除的组合，且无生命重排");
}
function reshuffle(free){
 const kinds=[];
 for(let y=1;y<=ROWS;y++)for(let x=1;x<=COLS;x++)if(grid[y][x]>=0)kinds.push(grid[y][x]);
 let tries=0;
 do{
  const d=shuffled(kinds.slice());let i=0;
  for(let y=1;y<=ROWS;y++)for(let x=1;x<=COLS;x++)if(grid[y][x]>=0)grid[y][x]=d[i++];
  renderAll();
  if(findHint())break;
 }while(++tries<50);
 play("shuffle");
}
// ===== 提示 =====
function clearHintFlash(){document.querySelectorAll(".tile.hint").forEach(e=>e.classList.remove("hint"));}
function doHint(){
 if(paused||over)return;
 const h=findHint();
 if(!h){toast("没有可消除的组合");return;}
 if(hints>0){hints--;updUI();}
 clearHintFlash();
 const e1=tiles.get(h.a[0]+","+h.a[1]),e2=tiles.get(h.b[0]+","+h.b[1]);
 if(e1)e1.classList.add("hint");if(e2)e2.classList.add("hint");
 drawPath(h.path,"#ff5252");play("hint");
 setTimeout(()=>{clearHintFlash();fctx.clearRect(0,0,fx.width,fx.height);},3000);
}
// ===== 计时 =====
function startTimer(){
 clearInterval(timer);
 timer=setInterval(()=>{
  if(paused||over)return;
  remain=Math.max(0,remain-0.1);
  if(remain<=10&&Math.abs(remain%1)<0.05)play("tick");
  updTime();
  if(remain<=0)gameOver("时间到！");
 },100);
}
function gameOver(msg){
 over=true;clearInterval(timer);play("gameover");
 $("ovMsg").textContent=msg+`　最终得分：${score}`;
 $("overlay").classList.remove("hidden");
}
function winGame(){
 over=true;clearInterval(timer);play("win");
 $("ovMsg").textContent=`🎉 全部 ${MAX_LEVEL} 关通关！总分 ${score}`;
 $("overlay").classList.remove("hidden");
}
// ===== UI =====
function updUI(){
 $("lv").textContent=level;$("lay").textContent=LAYOUTS[(level-1)%LAYOUTS.length].name;
 $("lives").textContent=lives;$("hints").textContent=hints;$("score").textContent=score;
 $("diffName").textContent=DIFF[diff].name;updTime();
}
function updTime(){
 const total=levelTime(),p=Math.max(0,remain/total*100);
 const bar=$("timebar");bar.style.width=p+"%";
 bar.classList.toggle("low",remain<=20);
}
// ===== 暂停 =====
function togglePause(){
 if(over)return;
 paused=!paused;
 $("pauseMask").style.display=paused?"flex":"none";
 boardEl.style.visibility=paused?"hidden":"visible";
 $("pauseBtn").textContent=paused?"继续":"暂停";
}
// ===== 事件 =====
$("hintBtn").onclick=doHint;
$("shuffleBtn").onclick=()=>{if(paused||over)return;if(lives<=1){toast("生命不足！");play("error");return;}lives--;reshuffle();updUI();};
$("pauseBtn").onclick=togglePause;
document.addEventListener("keydown",e=>{
 if(e.key==="p"||e.key==="P"||e.key==="Enter")togglePause();
 if(e.key==="l"||e.key==="L"){ // 测试用：跳到下一关
  if(over)return;
  clearInterval(timer);nextLevel();startTimer();
 }
});
// 棋盘上任意右键都阻止默认菜单（含空白区域）
document.getElementById("boardWrap").addEventListener("contextmenu",e=>{e.preventDefault();onRightClick();});
$("soundBtn").onclick=()=>{soundOn=!soundOn;$("soundBtn").textContent=soundOn?"🔊 音效开":"🔇 音效关";};
$("menuBtn").onclick=()=>{over=true;clearInterval(timer);$("overlay").classList.remove("hidden");$("ovMsg").textContent="";};
$("startBtn").onclick=()=>{
 diff=+$("diffSel").value;tileSet=$("setSel").value;
 startLevel=+$("levelSel").value||1;
 localStorage.setItem("llk_tileset",tileSet);
 $("overlay").classList.add("hidden");newGame();
};
// 初始化起始关卡下拉框（1~MAX_LEVEL，显示牌型名）
(function(){
 const sel=$("levelSel");
 for(let i=1;i<=MAX_LEVEL;i++){
  const opt=document.createElement("option");
  opt.value=i;
  opt.textContent=`第${i}关（${LAYOUTS[(i-1)%LAYOUTS.length].name}）`;
  sel.appendChild(opt);
 }
})();
boardEl.style.position="relative";
