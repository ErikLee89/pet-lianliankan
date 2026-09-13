import struct, os
p_ = r"D:\Program Files (x86)\宠物连连看\midi"
for name in ["101","102","103","104"]:
    data = open(os.path.join(p_, name+".mid"),"rb").read()
    hdrlen,fmt,ntrk,div = struct.unpack_from(">IHHH", data, 4)
    print(name, "fmt",fmt,"ntrk",ntrk,"div",div,"size",len(data))
