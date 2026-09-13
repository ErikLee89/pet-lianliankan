const fs=require('fs');
const html=fs.readFileSync('D:/test/lianliankan/index.html','utf8');
let js=html.match(/<script>([\s\S]*?)<\/script>/)[1];
const elements={};
function makeEl(tag){return {tag,children:[],style:{},dataset:{},classList:{_s:new Set(),add(c){this._s.add(c)},remove(c){this._s.delete(c)},toggle(){},contains(){return false}},innerHTML:'',appendChild(c){return c},addEventListener(){},querySelectorAll(){return[]},getContext(){return{clearRect(){},beginPath(){},moveTo(){},lineTo(){},stroke(){}}},set onclick(f){},set oncontextmenu(f){},width:0,height:0};}
const byId={};
global.document={getElementById(id){if(!byId[id])byId[id]=makeEl('div');return byId[id];},createElement(t){return makeEl(t);},querySelectorAll(){return[]},addEventListener(){},body:makeEl('body')};
global.window={};global.localStorage={getItem(){return null},setItem(){}};
global.Audio=function(){return{play(){},pause(){},cloneNode(){return{play(){}}},currentTime:0,volume:1,loop:false}};
global.Image=function(){return{set src(v){},onload:null}};
global.requestAnimationFrame=()=>{};
js+=`;globalThis.__api={compactRow,set grid(v){grid=v},get grid(){return grid},set tiles(v){tiles=v},get tiles(){return tiles},set moveTileElFn(f){moveTileEl=f}};`;
// moveTileEl 是顶层 function，无法直接覆盖。先检测它的定义
console.log("moveTileEl 定义位置:",js.indexOf("function moveTileEl"));
eval(js);
const A=globalThis.__api;
// 检测 moveTileEl 是否存在于 eval 后
console.log("moveTileEl typeof:",typeof moveTileEl);
