import zlib
import struct
import os

#presumptions: we're gathering several files of whatever type and compressing
# them into one .zda file, with the same name as the directory they're in

#I think I'll do one .zda file at a time for simplicity, and have a wrapper
# with a loop to do more than one if I want

folders = [f for f in os.listdir() if not os.path.isfile(f) and f != 'ZDA']
print(folders)

for fold in folders:
    entries = []
    with open(fold+".zda", "wb") as out:
        files = os.listdir("./"+fold) # consider making this recursive, it just breaks if there are subfolders
        files.sort()
        start = 12+52*len(files)
        out.seek(start) #no header yet, need compression info below
        for f in files:
            eAddr = out.tell() - start
            with open(f'./{fold}/{f}', "rb") as incoming:
                eCsze = out.write(zlib.compress(incoming.read()))
                eDsze = incoming.tell()
                entries.append([f, eDsze, eCsze, eAddr])
        out.seek(0)
        out.write(struct.pack("4s", "ZDA".encode("utf-8")))
        out.write(struct.pack("<II", len(files), 12+52*len(files)))
        for e in entries:
            out.write(struct.pack("<40s3I", e[0].encode("utf-8"), e[1], e[2], e[3]))

def xor(first:str, second:str) -> str:
    first = str(first)
    second = str(second)
    return str(hex(int(first,16)^int(second,16)))[2:]
