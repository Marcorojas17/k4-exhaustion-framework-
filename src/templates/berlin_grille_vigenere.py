from src.core.base_engine import BaseCryptoEngine

def berlin_mask(h):
    mask=[]
    for i in range(14):
        for j in range(7):
            if ((i*j + h) % 7 ==0) or ((i+j+h)%5==0):
                mask.append(1)
            else: mask.append(0)
    return mask[:97]

def apply_grille(ct, hour, rot):
    mask=berlin_mask(hour)
    for _ in range(rot): mask=mask[7:]+mask[:7]
    pt=['']*97
    idx=0
    for i,m in enumerate(mask):
        if m==1 and idx<len(ct):
            pt[i]=ct[idx]; idx+=1
    for i,m in enumerate(mask):
        if m==0 and idx<len(ct):
            pt[i]=ct[idx]; idx+=1
    return ''.join(pt)

class BerlinGrilleVigenereEngine(BaseCryptoEngine):
    @property
    def name(self): return "BerlinGrilleVigenere"
    def decrypt(self, ct, key):
        hour, rot, vkey = key
        t1=apply_grille(ct,hour,rot)
        res=[]
        for i,ch in enumerate(t1):
            c=ord(ch)-65; k=ord(vkey[i%len(vkey)])-65
            p=(c - k) % 26
            res.append(chr(p+65))
        return ''.join(res)
    def get_key_generator(self):
        for h in range(24):
            for rot in range(4):
                for vk in ["BERLIN","KRYPTOS","CLOCK","BERLINCLOCK"]:
                    yield (h,rot,vk)

