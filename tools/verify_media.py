from pathlib import Path
import json
import subprocess
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
sheet = np.array(Image.open(ROOT / 'res/bmp_129.png').convert('RGB'))
for i in range(42):
    sprite = np.array(Image.open(ROOT / f'assets/tiles/pet_{i:02d}.png'))
    assert np.array_equal(sprite[:, :, :3], sheet[i*39:(i+1)*39,156:195])
    assert np.array_equal(sprite[:, :, 3] > 0,
                          sheet[i*39:(i+1)*39,195:234].mean(axis=2) < 128)
for i in range(101,118):
    subprocess.run(['ffmpeg','-v','error','-i',str(ROOT / f'assets/bgm/{i}.mp3'),
                    '-f','null','-'],check=True, capture_output=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width':1100,'height':850})
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto((ROOT / 'index.html').as_uri(),wait_until='networkidle')
    page.locator('#startBtn').click()
    page.locator('#bgmBtn').click()
    page.wait_for_function('!bgmAudio.paused && bgmAudio.currentTime > 0.2')
    page.locator('#pauseBtn').click()
    assert page.evaluate('bgmAudio.paused')
    elapsed = page.evaluate('bgmAudio.currentTime')
    page.locator('#pauseBtn').click()
    page.wait_for_function(f'!bgmAudio.paused && bgmAudio.currentTime > {elapsed}')
    original = page.evaluate('bgmIdx')
    page.evaluate('bgmAudio.currentTime=bgmAudio.duration-0.1')
    page.wait_for_function(f'bgmIdx===({original}+1)%17 && !bgmAudio.paused && bgmAudio.currentTime>0.1')
    page.locator('#bgmBtn').click()
    assert page.evaluate('bgmAudio.paused')
    page.locator('#bgmBtn').click()
    page.wait_for_function('!bgmAudio.paused')
    assert page.locator('.tile img').evaluate_all('(imgs)=>imgs.every(i=>i.complete && i.naturalWidth===64 && getComputedStyle(i).imageRendering==="auto")')
    page.screenshot(path=str(ROOT / 'verify/game-restored.png'), full_page=True)
    # Load metadata for every track through the same browser media pipeline.
    tracks = page.evaluate('''async()=>{const out=[]; for(const src of BGM_FILES){
      const a=new Audio();a.preload='metadata';
      await new Promise((resolve,reject)=>{a.onloadedmetadata=resolve;a.onerror=reject;a.src=src;});
      out.push({src,duration:a.duration});a.removeAttribute('src');a.load();
    }return out;}''')
    assert len(tracks)==17 and all(t['duration']>1 for t in tracks)
    page.locator('#menuBtn').click()
    assert page.evaluate('bgmAudio.paused')
    assert not errors, errors
    browser.close()
(ROOT / 'verify/media-test.json').write_text(json.dumps({
    'sprite_checks':42,'mp3_full_decode_checks':17,'browser_tracks':tracks,
    'play_pause_resume_end_next_toggle_menu':'passed','page_errors':errors,
},indent=2),encoding='utf-8')
print('PASS: 42 sprites, 17 full MP3 decodes, browser playback/pause/resume/next/off/menu.')
