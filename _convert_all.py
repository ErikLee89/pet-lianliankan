import struct, wave, os, sys, glob

SRC = r"D:\Program Files (x86)\宠物连连看\midi"
OUT = r"D:\test\lianliankan\assets\bgm"
os.makedirs(OUT, exist_ok=True)

def read_midi(path):
    data = open(path, "rb").read()
    p = 0
    def u32():
        nonlocal p
        v = struct.unpack_from(">I", data, p)[0]; p += 4; return v
    def u16():
        nonlocal p
        v = struct.unpack_from(">H", data, p)[0]; p += 2; return v
    def u8():
        nonlocal p
        v = data[p]; p += 1; return v
    def varlen():
        nonlocal p
        v = 0
        while True:
            b = data[p]; p += 1
            v = (v << 7) | (b & 0x7F)
            if not (b & 0x80): break
        return v
    if data[:4] != b"MThd": raise ValueError("not midi")
    u32(); fmt = u16(); ntrk = u16(); div = u16()
    tempo_ev = []; tracks = []
    for t in range(ntrk):
        if data[p:p+4] != b"MTrk": raise ValueError("bad trk")
        p += 4
        ln = u32(); end = p + ln
        tick = 0; ev = []
        while p < end:
            tick += varlen()
            st = data[p]
            if st == 0xFF:
                p += 1; typ = u8(); n = varlen()
                if typ == 0x51:
                    us = (data[p]<<16)|(data[p+1]<<8)|data[p+2]
                    tempo_ev.append((tick, us))
                p += n
            elif st in (0xF0, 0xF7):
                p += 1; n = varlen(); p += n
            else:
                cmd = st & 0xF0; ch = st & 0x0F
                if cmd in (0x90, 0x80):
                    note, vel = u8(), u8()
                    ev.append((tick, cmd, ch, note, vel))
                elif cmd in (0xC0, 0xD0):
                    p += 1
                elif cmd in (0xB0, 0xE0, 0xA0):
                    p += 2
                else:
                    break
        p = end
        tracks.append(ev)
    tempo_ev.sort(key=lambda x: x[0])
    # tick -> seconds
    def make_t2s():
        segs = []; cu = 500000; ct = 0; cs = 0.0
        for tick, us in tempo_ev:
            dt = tick - ct
            if dt < 0: continue
            cs += dt * cu / div / 1e6
            ct = tick; cu = us
            segs.append((ct, cs, cu))
        if not segs: segs = [(0, 0.0, 500000)]
        def t2s(tick):
            us = 500000; tt = 0; ss = 0.0
            for g in segs:
                if g[0] <= tick: us, tt, ss = g[1], g[0], g[2]
                else: break
            return ss + (tick - tt) * us / div / 1e6
        return t2s
    return tracks, make_t2s()

def render(midi_path, wav_path, sr=22050):
    tracks, t2s = read_midi(midi_path)
    notes = []
    for ev in tracks:
        on = {}
        for tick, cmd, ch, note, vel in ev:
            key = (ch, note)
            if cmd == 0x90 and vel > 0:
                on[key] = (t2s(tick), vel, ch, note)
            elif cmd == 0x80 or (cmd == 0x90 and vel == 0):
                o = on.pop(key, None)
                if o:
                    notes.append((o[0], t2s(tick) - o[0], o[1], o[2], o[3]))
    for k, o in list(on.items()) if False else []: pass
    if not notes:
        print(f"  SKIP {os.path.basename(midi_path)} (no notes)"); return False
    total = max(t + d for t, d, *_ in notes) + 1.0
    n = int(total * sr)
    buf = [0.0] * n
    import math, random
    random.seed(7)
    for t, dur, vel, ch, note in notes:
        if dur <= 0: dur = 0.4
        f = 440.0 * 2 ** ((note - 69) / 12)
        if ch == 9:
            vol = (vel/127) * 0.10
            d = min(dur, 0.15); s = int(t*sr); ln = max(1, int(d*sr))
            for i in range(ln):
                if s+i >= n: break
                buf[s+i] += vol * math.exp(-i/sr*30) * (random.random()*2-1)
            continue
        vol = (vel/127) * 0.16
        if ch == 1: vol *= 1.3
        atk = min(0.02, dur/4); rel = min(0.35, max(0.1, dur/2))
        s = int(t*sr); ln = int((dur+rel)*sr)
        for i in range(ln):
            j = s + i
            if j >= n: break
            tt = i/sr
            if tt < atk: env = tt/atk
            elif tt < dur: env = 1.0
            else: env = max(0.0, 1-(tt-dur)/rel)
            w = math.sin(2*math.pi*f*tt) + 0.25*math.sin(2*math.pi*f*2*tt)
            buf[j] += vol * env * w
    peak = max(1e-6, max(abs(x) for x in buf))
    k = 0.85/peak
    with wave.open(wav_path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(b"".join(struct.pack("<h", max(-32768, min(32767, int(x*k*32767)))) for x in buf))
    return True

import lameenc
ok = 0
for mid in sorted(glob.glob(os.path.join(SRC, "*.mid"))):
    name = os.path.splitext(os.path.basename(mid))[0]
    wav = os.path.join(OUT, f"_tmp_{name}.wav")
    mp3 = os.path.join(OUT, f"{name}.mp3")
    try:
        if not render(mid, wav): continue
        pcm = open(wav, "rb").read()
        enc = lameenc.Encoder()
        enc.set_bit_rate(96); enc.set_in_sample_rate(22050)
        enc.set_channels(1); enc.set_quality(5)
        data = enc.encode(pcm) + enc.flush()
        open(mp3, "wb").write(data)
        os.remove(wav)
        ok += 1
        print(f"OK {name}.mp3  {os.path.getsize(mp3)//1024}KB")
    except Exception as e:
        print(f"FAIL {name}: {e}")
print(f"done: {ok}/17")
