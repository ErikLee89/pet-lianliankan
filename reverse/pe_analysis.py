import sys
sys.path.insert(0,r'D:\test\lianliankan\tools\reverse_deps')
import pefile,capstone
from pathlib import Path
p=pefile.PE(r'D:\Program Files (x86)\llkwqb\zzllk.exe')
print(hex(p.OPTIONAL_HEADER.ImageBase),hex(p.OPTIONAL_HEADER.AddressOfEntryPoint))
for s in p.sections: print(s.Name,hex(s.VirtualAddress),s.SizeOfRawData)
for d in p.DIRECTORY_ENTRY_IMPORT:
 print(d.dll.decode(),[(hex(i.address),i.name.decode() if i.name else i.ordinal) for i in d.imports])
m=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_32);m.skipdata=True
out=[]
for s in p.sections:
 if s.Characteristics&0x20000000:
  out.extend(f'{i.address:08x} {i.mnemonic} {i.op_str}' for i in m.disasm(s.get_data(),p.OPTIONAL_HEADER.ImageBase+s.VirtualAddress))
Path(r'D:\test\lianliankan\reverse\disassembly.txt').write_text('\n'.join(out))
