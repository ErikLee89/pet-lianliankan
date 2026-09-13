const KIND_COUNT = 42;
const POOL_SIZES = [21, 28, 35, 42];
function shuffled(a){for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;}
function kinds48(diff){
 const pool = POOL_SIZES[diff] || 21;
 const order = shuffled([...Array(pool).keys()]);
 const ks = [];
 for(let i = 0; i < 12*8/2; i++) ks.push(order[i % pool]);
 return ks;
}
for(let d = 0; d < 4; d++){
 const k = kinds48(d);
 const uniq = new Set(k);
 const maxId = Math.max(...uniq);
 console.log(`难度${d}: 48对牌，用到 ${uniq.size} 种图案，最大编号 ${maxId}`);
 // 每种应出现1-3次（48对 / pool种）
 const cnt = {};
 k.forEach(v => cnt[v] = (cnt[v]||0)+1);
 const freq = Object.values(cnt);
 console.log(`   每种出现次数范围: ${Math.min(...freq)}~${Math.max(...freq)}`);
}
