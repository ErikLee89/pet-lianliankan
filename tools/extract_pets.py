"""Extract original RGB sprites using their paired Windows bitmap masks."""
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sheet = np.array(Image.open(ROOT / 'res/bmp_129.png').convert('RGB'))
preview = Image.new('RGBA', (7 * 78, 6 * 78), (255, 200, 225, 255))
for i in range(42):
    rgb = sheet[i*39:(i+1)*39, 4*39:5*39]
    mask = sheet[i*39:(i+1)*39, 5*39:6*39]
    # A few later masks contain near-black/near-white pixels; classify the mask,
    # never the sprite colors, so black eyes and outlines remain opaque.
    alpha = np.where(mask.mean(axis=2) < 128, 255, 0).astype('uint8')
    sprite = Image.fromarray(np.dstack((rgb, alpha)))
    sprite.save(ROOT / f'assets/tiles/pet_{i:02d}.png')
    preview.alpha_composite(sprite.resize((78, 78), Image.Resampling.NEAREST),
                            ((i % 7) * 78, (i // 7) * 78))
preview.convert('RGB').save(ROOT / 'verify/pets-restored.png')
print('Extracted 42 pets with original masks.')
