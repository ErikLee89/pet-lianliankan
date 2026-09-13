import sys
sys.path.insert(0,r'D:\test\lianliankan\tools\reverse_deps')
import pefile,hashlib
from pathlib import Path
p=pefile.PE(r'D:\Program Files (x86)\llkwqb\zzllk.exe')
for a in range(0x446500,0x4466a0):
 if p.get_data(a-0x400001,1)==b'\0':
  s=p.get_string_at_rva(a-0x400000)
  if len(s)>2:
   try: print(hex(a),s.decode('gbk'))
   except: pass
for t in p.DIRECTORY_ENTRY_RESOURCE.entries:
 if str(t.name)=='WAVE':
  for e in t.directory.entries:
   z=e.directory.entries[0].data.struct
   raw=p.get_data(z.OffsetToData,z.Size)
   matches=[x.name for x in Path(r'D:\test\lianliankan\assets\sfx').glob('*.wav') if x.read_bytes()==raw]
   print(e.id,matches)
