import struct, os, glob
import numpy as np

RES = r"D:\test\lianliankan\res"
OUT = r"D:\test\lianliankan\assets\bgm"
os.makedirs(OUT, exist_ok=True)

def read_vl(data, pos):
    val = 0
    while True:
        b = data[pos]; pos += 1
        val = (val << 7) | (b & 0x7F)
        if not (b & 0x80): break
    return val, pos

def parse_midi(path):
    data = open(path, "rb").read()
    assert data[:4] == b"MThd"
    hdr_len = struct.unpack(">I", data[4:8])[0]
    fmt, ntrk, division = struct.unpack(">HHH", data[8:14])
    pos = 8 + hdr_len
    tempos = [(0, 500000)]
    events_all = []  # (tick, type, note, vel, ch)
    for trk in range(ntrk):
        if data[pos:pos+4] != b"MTrk": break
        tlen = struct.unpack(">I", data[pos+4:pos+8])[0]
        end = pos + 8 + tlen
        p = pos + 8
        tick = 0; running = None
        while p < end:
            dt, p = read_vl(data, p)
            tick += dt
            b = data[p]
            if b & 0x80:
                p += 1; running = b
            else:
                b = running
            if b == 0xFF:
                meta = data[p]; p += 1
                ln, p = read_vl(data, p)
                if meta == 0x51 and ln == 3:
                    us = struct.unpack(">I", b"\x00"+data[p:p+3])[0]
                    tempos.append((tick, us))
                p += ln
            elif b in (0x90, 0x80):
                note, vel = data[p], data[p+1]; p += 2
                events_all.append((tick, b, note, vel))
            elif b in (0xA0,0xB0,0xE0):
                p += 2
            elif b in (0xC0,0xD0):
                p += 1
            elif b == 0xF0 or b == 0xF7:
                ln, p = read_vl(data, p); p += ln
            else:
                p += 1
        pos = end
    return events_all, tempos, division

def render(events, tempos, division, sr=22050):
    tempos.sort()
    events.sort(key=lambda e: e[0])
    def tick2sec(t):
        us = 500000
        for tt, u in tempos:
            if tt <= t: us = u
            else: break
        return t * us / 1e6 / max(division, 1)
    # note on/off 配对
    notes = []
    ons = {}
    for tick, typ, note, vel in events:
        if typ == 0x90 and vel > 0:
            ons.setdefault(note, []).append((tick, vel))
        elif typ == 0x80 or (typ == 0x90 and vel == 0):
            if ons.get(note):
                st, v = ons[note].pop(0)
                notes.append((tick2sec(st), max(tick2sec(tick) - tick2sec(st), 0.05), note, v))
    if not notes: return None
    total = max(st + du for st, du, _, _ in notes) + 1.0
    n = int(total * sr)
    audio = np.zeros(n, dtype=np.float32)
    for st, du, note, vel in notes:
        f = 440.0 * 2 ** ((note - 69) / 12)
        ln = int(du * sr)
        if ln <= 0: continue
        t = np.arange(ln, dtype=np.float32) / sr
        env = np.minimum(t / 0.01, 1) * np.exp(-t * 2.5)
        w = (np.sin(2*np.pi*f*t) + 0.35*np.sin(4*np.pi*f*t) + 0.15*np.sin(6*np.pi*f*t)).astype(np.float32)
        s = w * env * (vel / 127.0) * 0.25
        i0 = int(st * sr)
        i1 = min(i0 + ln, n)
        audio[i0:i1] += s[:i1-i0]
    peak = np.abs(audio).max()
    if peak > 0: audio = audio / peak * 0.85
    return audio, int(total)

def save_wav(path, audio, sr):
    d = (np.clip(audio, -1, 1) * 32767).astype("<i2").tobytes()
    with open(path, "wb") as f:
        f.write(b"RIFF"); f.write(struct.pack("<I", 36 + len(d)))
        f.write(b"WAVEfmt "); f.write(struct.pack("<IHHIIHH", 16, 1, 1, sr, sr*2, 2, 16))
        f.write(b"data"); f.write(struct.pack("<I", len(d))); f.write(d)

mids = sorted(glob.glob(os.path.join(RES, "mid_*.mid"))) or sorted(glob.glob(os.path.join(r"D:\test\lianliankan\midi_src", "*.mid")))
# 直接从原程序 midi 文件夹取前几首
src_dir = r"D:\Program Files (x86)\宠物连连看\midi"
mids = sorted(glob.glob(os.path.join(src_dir, "*.mid")))[:5]
report = []
for m in mids:
    try:
        ev, tempos, div = parse_midi(m)
        r = render(ev, tempos, div)
        if not r: continue
        audio, total = r
        out = os.path.join(OUT, os.path.splitext(os.path.basename(m))[0] + ".wav")
        save_wav(out, audio, 22050)
        report.append(f"{os.path.basename(m)} -> {os.path.basename(out)} {total}s {os.path.getsize(out)}B")
    except Exception as e:
        report.append(f"{os.path.basename(m)} FAIL: {e}")
print("\n".join(report))
print("OUTPUT_DIR=" + OUT)
