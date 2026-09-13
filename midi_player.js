// ===== 迷你 MIDI 播放器（Web Audio 实时合成）=====
// 用法: const p=new MidiPlayer(); await p.load("assets/bgm/102.mid"); p.play();
//     p.stop(); p.onended=...;
const MidiPlayer=(()=>{
  const NOTE_OFFSET={c:0,d:2,e:4,f:5,g:7,a:9,b:11};
  // --- MIDI 解析 ---
  function parseMidi(buf){
    const v=new DataView(buf); let p=0;
    const u32=()=>{const x=v.getUint32(p);p+=4;return x}, u16=()=>{const x=v.getUint16(p);p+=2;return x}, u8=()=>v.getUint8(p++);
    if(u32()!==0x4d546864)throw "not midi";
    u32(); const fmt=u16(), ntrk=u16(), div=u16(); // division (ticks per quarter)
    const tempoEvents=[], tracks=[];
    for(let t=0;t<ntrk;t++){
      if(u32()!==0x4d54726b)throw "bad trk";
      const len=u32(), end=p+len; let tick=0, run=0;
      const ev=[];
      while(p<end){
        // varlen
        let d=0,b; do{b=u8();d=(d<<7)|(b&0x7f);}while(b&0x80);
        tick+=d; const st=u8();
        if(st===0xFF){const type=u8();let n=0;do{b=u8();n=(n<<7)|(b&0x7f);}while(b&0x80);
          if(type===0x51){ // tempo
            let us=0; for(let i=0;i<3;i++)us=(us<<8)|u8(); tempoEvents.push({tick,us});
          } else p+=n;
        } else if(st===0xF0||st===0xF7){let n=0;do{b=u8();n=(n<<7)|(b&0x7f);}while(b&0x80);p+=n;}
        else{
          const cmd=st&0xF0, ch=st&0x0F;
          if(cmd===0x90||cmd===0x80){const note=u8(),vel=u8(); ev.push({tick,st,cmd,ch,note,vel});}
          else if(cmd===0xC0||cmd===0xD0){u8();}
          else if(cmd===0xB0||cmd===0xE0||cmd===0xA0){u8();u8();}
          else {/*running status unsupported*/break;}
        }
      }
      p=end; tracks.push(ev);
    }
    tempoEvents.sort((a,b)=>a.tick-b.tick);
    // tick -> seconds
    const defaultUs=500000; // 120bpm
    let us=defaultUs, lastTick=0, lastSec=0;
    const tick2sec=tick=>{
      let s=lastSec+(tick-lastTick)*us/div/1e6;
      // (tempo changes handled via cumulative pass below)
      return s;
    };
    // build tempo map segments
    const segs=[]; let curUs=500000, curTick=0, curSec=0;
    for(const te of tempoEvents){
      const dt=te.tick-curTick; if(dt<0)continue;
      curSec+=dt*curUs/div/1e6; curTick=te.tick; curUs=te.us;
      segs.push({tick:curTick,sec:curSec,us:curUs});
    }
    const t2s=tick=>{
      let s=curSec0(tick); return s;
      function curSec0(t){let useg=500000,tt=0,ss=0;
        for(const g of segs){ if(g.tick<=t){}else break; useg=g.us;tt=g.tick;ss=g.sec;}
        if(tt===t)return ss; return ss+(t-tt)*useg/div/1e6;}
    };
    // Alternative simpler correct implementation:
    const tickToSec=(()=>{ // precompute cumulative
      let acc=0, t=0, usAt=500000; const map=[]; const evs=[...tempoEvents];
      let i=0;
      return tick=>{
        // walk forward caching state in closure vars
        while(i<evs.length&&evs[i].tick<=tick){acc+=(evs[i].tick-t)*usAt/div/1e6;t=evs[i].tick;usAt=evs[i].us;i++;}
        return acc+(tick-t)*usAt/div/1e6;
      };
    })();
    // notes
    const notes=[];
    for(const tr of tracks){
      const on={};
      for(const e of tr){
        const key=e.ch*128+e.note;
        if(e.cmd===0x90&&e.vel>0){on[key]={t:tickToSec(e.tick),vel:e.vel,ch:e.ch,note:e.note};}
        else if(e.cmd===0x80||(e.cmd===0x90&&e.vel===0)){const o=on[key]; if(o){o.dur=tickToSec(e.tick)-o.t; o.prog=e.ch===9?118:0;notes.push(o);delete on[key];}}
      }
      for(const k in on){const o=on[k];o.dur=0.5;notes.push(o);}
    }
    notes.sort((a,b)=>a.t-b.t);
    let total=0; for(const n of notes)total=Math.max(total,n.t+n.dur);
    return {div,notes,total:Math.max(total,1)};
  }
  // --- 合成 ---
  const midi2freq=n=>440*Math.pow(2,(n-69)/12);
  const CH_ACOUSTIC=0, CH_BASS=1, CH_LEAD=2, CH_PAD=3;
  function noteWave(ctx,when,freq,dur,vel,ch,prog){
    const g=ctx.createGain(), o=ctx.createOscillator(), o2=ctx.createOscillator();
    const vol=(vel/127)*(ch===9?0.10:(ch===CH_BASS?0.22:0.16));
    let type="triangle", det=0, f=freq, f2=freq*2;
    if(ch===9){ // drums: simple noise-ish blip on percussion
      const nb=ctx.createOscillator(); nb.type="square"; nb.frequency.value=freq<100?80:freq/4;
      const ng=ctx.createGain(); ng.gain.setValueAtTime(vol,when); ng.gain.exponentialRampToValueAtTime(0.001,when+Math.min(dur,0.15));
      nb.connect(ng).connect(ctx.destination); nb.start(when); nb.stop(when+Math.min(dur,0.2)); return;
    }
    if(prog>0){} // could vary by program; keep simple
    o.type=type; o.frequency.value=f;
    o2.type="sine"; o2.frequency.value=f2; 
    const g2=ctx.createGain(); g2.gain.value=0.25;
    const atk=Math.min(0.02,dur/4), rel=ch===CH_PAD?Math.min(0.6,dur):Math.min(0.35,Math.max(0.1,dur/2));
    g.gain.setValueAtTime(0,when);
    g.gain.linearRampToValueAtTime(vol,when+atk);
    g.gain.setValueAtTime(vol,when+dur);
    g.gain.exponentialRampToValueAtTime(0.001,when+dur+rel);
    o.connect(g); o2.connect(g2).connect(g);
    g.connect(ctx.destination);
    o.start(when); o.stop(when+dur+rel+0.05);
    o2.start(when); o2.stop(when+dur+rel+0.05);
  }
  class Player{
    constructor(){this.ctx=null;this.buf=null;this.timer=null;this.playing=false;this.onended=null;this.off=0;}
    async load(url){
      const r=await fetch(url); if(!r.ok)throw "fetch fail";
      this.parsed=parseMidi(await r.arrayBuffer());
    }
    play(){
      this.stop();
      if(!this.parsed)return;
      this.ctx=this.ctx||new (window.AudioContext||window.webkitAudioContext)();
      this.ctx.resume&&this.ctx.resume();
      this.playing=true; this.t0=this.ctx.currentTime+0.15; this.i=0;
      const LOOK=1.2;
      const pump=()=>{
        if(!this.playing)return;
        const now=this.ctx.currentTime-this.t0, parsed=this.parsed;
        while(this.i<parsed.notes.length&&parsed.notes[this.i].t<now+LOOK){
          const n=parsed.notes[this.i++];
          noteWave(this.ctx,this.t0+n.t,midi2freq(n.note),Math.max(0.05,n.dur),n.vel,n.ch,n.prog);
        }
        if(now>parsed.total+0.8){this.playing=false;this.onended&&this.onended();return;}
        this.timer=setTimeout(()=>pump(),200);
      };
      pump();
      this._pump=pump;
    }
    stop(){this.playing=false;clearTimeout(this.timer);if(this.ctx)this.ctx.close().catch(()=>{}),this.ctx=null;}
  }
  return Player;
})();
