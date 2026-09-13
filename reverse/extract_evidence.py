import sys, json, hashlib, struct
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools/reverse_deps'))
import pefile,capstone
source=Path(r'D:\Program Files (x86)\llkwqb\zzllk.exe')
p=pefile.PE(str(source)); base=p.OPTIONAL_HEADER.ImageBase
m=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_32)
ranges=[('new_game_1_to_3',0x4049d0,0x404b10),('new_game_4',0x408250,0x4082b8),('match_score_time',0x404d00,0x404d66),('level_bonus',0x404e58,0x404e9d),('next_level_resources',0x405010,0x40503e),('final_bonus',0x40508a,0x4050d5),('timer',0x405600,0x405850),('hint',0x406020,0x406080),('shuffle',0x4064f0,0x406547),('events_1_to_3',0x4080c0,0x408232),('events_4',0x4088d0,0x408a29),('rand',0x41e7f7,0x41e819)]
lines=[]
for title,start,end in ranges:
 lines.append('\n## '+title)
 lines.extend(f'{i.address:08x} {i.mnemonic} {i.op_str}' for i in m.disasm(p.get_data(start-base,end-start),start))
for addr in [0x408234,0x408a2c]:
 lines.append(f'\nJump table {addr:08x}: '+', '.join(hex(x) for x in struct.unpack('<7I',p.get_data(addr-base,28))))
for addr in [0x4465bc,0x4465d0,0x4465e4,0x4465f8,0x44660c,0x446620,0x446638,0x446650,0x446664,0x446678,0x446690,0x4467cc]:
 lines.append(f'{addr:08x}: '+p.get_string_at_rva(addr-base).decode('gbk'))
Path(__file__).with_name('rule_evidence.txt').write_text('\n'.join(lines),encoding='utf-8')
print('Evidence written; original SHA256',hashlib.sha256(source.read_bytes()).hexdigest())
