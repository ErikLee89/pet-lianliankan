"""Render the original MIDI files with FluidSynth, then encode browser-ready MP3s."""
from pathlib import Path
import concurrent.futures
import json
import shutil
import subprocess
import wave

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(r'D:\Program Files (x86)\llkwqb\midi')
SYNTH = ROOT / 'tools/audio/fluidsynth/bin/fluidsynth.exe'
FONT = ROOT / 'tools/audio/TimGM6mb.sf2'
OUTPUT = ROOT / 'assets/bgm'

def convert(source):
    target = OUTPUT / (source.stem + '.mp3')
    wav = OUTPUT / (source.stem + '.render.wav')
    subprocess.run([str(SYNTH), '-ni', '-F', str(wav), '-r', '44100',
                    '-g', '0.5', str(FONT), str(source)], check=True,
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    with wave.open(str(wav)) as audio:
        duration = audio.getnframes() / audio.getframerate()
        assert duration > 1
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
                    '-i', str(wav), '-codec:a', 'libmp3lame', '-b:a', '192k',
                    str(target)], check=True)
    wav.unlink()
    print(f'{target.name}: {duration:.1f}s', flush=True)
    return {'file': target.name, 'seconds': round(duration, 3), 'bytes': target.stat().st_size}

if __name__ == '__main__':
    OUTPUT.mkdir(exist_ok=True)
    sources = sorted(SOURCE.glob('*.mid'))
    assert len(sources) == 17
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(convert, sources))
    (OUTPUT / 'conversion.json').write_text(json.dumps({
        'source': str(SOURCE), 'synthesizer': 'FluidSynth 2.4.7',
        'soundfont': 'TimGM6mb.sf2', 'tracks': results,
    }, indent=2), encoding='utf-8')
