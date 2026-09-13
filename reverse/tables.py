import sys,struct,re,hashlib
sys.path.insert(0,r'D:\test\lianliankan\tools\reverse_deps')
import pefile
p=pefile.PE(r'D:\Program Files (x86)\llkwqb\zzllk.exe')
for a in [0x408234,0x408a2c]: print(hex(a),[hex(x) for x in struct.unpack('<7I',p.get_data(a-0x400000,28))])
for a in range(0x446600,0x446900):
 b=p.get_data(a-0x400000,1)
 if a==0x446600 or p.get_data(a-0x400001,1)==b'\0':
  s=p.get_string_at_rva(a-0x400000)
  if len(s)>2:
   try: print(hex(a),s.decode('gbk'))
   except: pass
print('SHA256',hashlib.sha256(p.__data__).hexdigest())
