"""Generate 64px pet icons using the approved smooth preview settings."""
from pathlib import Path
from PIL import Image

root=Path(__file__).resolve().parents[1]
out=root/'assets/tiles_smooth64'
out.mkdir(exist_ok=True)
for i in range(42):
    name=f'pet_{i:02d}.png'
    source=Image.open(root/'assets/tiles'/name).convert('RGBA')
    source.convert('RGBa').resize((64,64),Image.Resampling.LANCZOS).convert('RGBA').save(out/name)
print('Generated 42 smooth 64x64 pet icons.')
