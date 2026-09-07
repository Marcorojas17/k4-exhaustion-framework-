import math
from src.core.base_engine import BaseCryptoEngine

def columnar_encrypt(text, perm):
    k=len(perm)
    n=len(text)
    rows=math.ceil(n/k)
    cols=['']*k
    idx=0
    for r in range(rows):
        for c in range(k):
            if idx < n:
                cols[c]+=text[idx]
                idx+=1
            else:
                cols[c]+=''
    # read in perm order
    out=''
    order=sorted(range(k), key=lambda x: perm[x])
    for c in order:
        out+=cols[c]
    return out

class BeaufortDoubleColumnarEngine(BaseCryptoEngine):
    @property
    def name(self): return "BeaufortDoubleColumnar"
    def decrypt(self, ct, key):
        perm1, perm2, bkey = key
        # 1. Beaufort first (undo beaufort = same)
        t0=[]
        for i,ch in enumerate(ct):
            c=ord(ch)-65
            k=ord(bkey[i % len(bkey)])-65
            p=(k - c) % 26
            t0.append(chr(p+65))
        t0=''.join(t0)
        # 2. undo col2 then col1? encryption was col1 then col2, so decrypt reverse
        # To invert, we need uncolumnar function
        def uncolumnar(text, perm):
            k=len(perm); n=len(text); rows=math.ceil(n/k)
            col_lens=[rows]*k
            rem=rows*k-n
            for i in range(rem): col_lens[k-1-i]-=1
            cols=['']*k; idx=0
            order=sorted(range(k), key=lambda x: perm[x])
            for c in order:
                l=col_lens[c]
                cols[c]=text[idx:idx+l]
                idx+=l
            out=[]
            for r in range(rows):
                for c in range(k):
                    if r < len(cols[c]): out.append(cols[c][r])
            return ''.join(out)
        t1=uncolumnar(t0, perm2)
        t2=uncolumnar(t1, perm1)
        return t2
    def get_key_generator(self):
        perms6=[(2,0,5,1,3,4),(1,0,5,6,3,2)]
        perms7=[(2,0,5,1,3,4,6)]
        bkeys=["BERLIN","CLOCK","BERLINCLOCK","KRYPTOS","SOTPYRK"]
        for p1 in perms6:
            for p2 in perms7:
                for bk in bkeys:
                    yield (p1,p2,bk)
                    yield (p2,p1,bk)

