from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    page=browser.new_page(viewport={'width':1100,'height':900})
    errors=[]
    page.on('pageerror',lambda e: errors.append(str(e)))
    page.goto((ROOT/'index.html').as_uri(),wait_until='networkidle')
    result=page.evaluate('''()=>{
      let checks=0;
      function assert(ok){if(!ok)throw Error('check '+checks);checks++;}
      const expected=[[12,7,21],[14,8,28],[16,9,36],[18,10,42]];
      for(diff=0;diff<4;diff++){
        newGame();clearInterval(timer);
        const [cols,rows,kinds]=expected[diff];
        assert(COLS===cols&&ROWS===rows&&tiles.size===cols*rows);
        const counts=new Map();grid.flat().filter(k=>k>=0).forEach(k=>counts.set(k,(counts.get(k)||0)+1));
        assert(counts.size===kinds);
        if(diff<3)assert([...counts.values()].every(n=>n===4));
        else{const extras=[...counts].filter(([k,n])=>n===6).map(([k])=>k).sort((a,b)=>a-b);assert(extras.length===6&&extras[5]-extras[0]===5&&[...counts.values()].every(n=>n===4||n===6));}
        assert(boardEl.offsetWidth===cols*TILE&&boardEl.offsetHeight===rows*TILE);
        for(level=1;level<=11;level++){
          buildBoard();
          // Remove corners, then ensure all remaining tiles survive each movement.
          for(const [x,y] of [[1,1],[COLS,ROWS]]){grid[y][x]=-1;tiles.get(x+','+y).remove();tiles.delete(x+','+y);}
          applyGravity();
          assert(tiles.size===cols*rows-2&&tilesLeft()===tiles.size);
          assert([...tiles].every(([key,el])=>{const [x,y]=key.split(',').map(Number);return Number.isInteger(x)&&Number.isInteger(y)&&x>=1&&x<=cols&&y>=1&&y<=rows&&grid[y][x]>=0&&+el.dataset.x===x&&+el.dataset.y===y;}));
        }
      }
      diff=3;newGame();clearInterval(timer);$('overlay').classList.add('hidden');return {checks,status:'passed'};
    }''')
    page.screenshot(path=str(ROOT/'verify/difficulty-highest.png'))
    assert not errors,errors
    print(result)
    browser.close()
