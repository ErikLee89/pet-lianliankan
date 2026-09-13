from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    page=browser.new_page()
    errors=[]
    page.on('pageerror',lambda e: errors.append(str(e)))
    page.goto((ROOT/'index.html').as_uri(),wait_until='networkidle')
    result=page.evaluate('''async()=>{
      let checks=0;
      function eq(actual,expected){if(JSON.stringify(actual)!==JSON.stringify(expected))throw Error(JSON.stringify({actual,expected}));checks++;}
      const sounds=[];play=(k,force)=>sounds.push([k,force]);
      for(diff=0;diff<4;diff++){newGame();clearInterval(timer);eq([lives,hints,remain],[diff+2,(diff+2)*2,300]);}
      const rand=originalRand;
      function event(d,b,extra=0,t=299,h=5){diff=d;remain=t;hints=h;lives=5;score=0;resetEvent();let draws=[b,extra];originalRand=()=>draws.shift();sounds.length=0;randomEvent();return [hints,lives,score,remain,sounds.at(-1)?.[0]||null];}
      const normal=[[7,5,0,299,'rewardLarge'],[5,5,2500,299,'rewardLarge'],[4,5,0,299,'punish'],[6,5,0,299,'reward'],[5,5,0,313,'reward'],[5,5,1000,299,'reward'],[5,5,0,285,'punish']];
      const special=[[7,5,0,299,'rewardLarge'],[9,5,0,299,'rewardTop'],[5,6,0,299,'reward'],[6,5,0,299,'reward'],[5,5,0,313,'reward'],[5,7,0,299,'rewardLarge'],[5,9,0,299,'rewardTop']];
      for(let d=0;d<4;d++)for(let b=0;b<7;b++)eq(event(d,b),d===3?special[b]:normal[b]);
      eq(event(0,2,1),[5,5,0,299,null]);eq(currentEvent,-1);
      eq(event(0,2,0,299,0),[0,5,0,299,null]);
      eq(event(0,6,0,59),[5,5,0,59,null]);
      eq(event(0,1,0,298),[5,5,0,298,null]);
      event(0,1);randomEvent();eq(score,2500);
      await new Promise(r=>setTimeout(r,3050));eq(currentEvent,-1);
      originalRand=rand;diff=0;newGame();clearInterval(timer);remain=1;timerTick();eq([remain,score,over],[0,0,false]);timerTick();eq([remain,score,over],[-1,100,true]);timerTick();eq(score,100);
      newGame();clearInterval(timer);paused=true;timerTick();eq(remain,300);paused=false;
      hints=0;sounds.length=0;doHint();eq(sounds.length,0);
      score=50;gameOver('deadlock');eq(score,50);
      newGame();clearInterval(timer);grid=emptyGrid();remain=123;lives=2;hints=4;score=10;checkState();eq(score,213);checkState();eq(score,213);eq(sounds.at(-1)[0],'win');
      $('clearOk').click();clearInterval(timer);eq([level,lives,hints,remain],[2,3,5,300]);
      level=11;grid=emptyGrid();remain=123;lives=2;hints=4;score=10;checkState();eq(score,213);eq(sounds.at(-1)[0],'winall');$('clearOk').click();eq([score,lives,hints,over],[213,2,4,true]);
      // Actual click path: leave another pair so event eligibility is evaluated.
      newGame();clearInterval(timer);grid=emptyGrid();grid[1][1]=0;grid[1][2]=0;grid[2][1]=1;grid[2][2]=1;renderAll();remain=298;onTile(1,1);onTile(2,1);await new Promise(r=>setTimeout(r,250));eq([score,remain],[10,302]);
      clearInterval(timer);resetEvent();return {checks,status:'passed'};
    }''')
    assert not errors,errors
    print(result)
    browser.close()
