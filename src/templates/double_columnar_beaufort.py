from itertools import permutations
import math
from src.core.base_engine import BaseCryptoEngine

# keywords que Sanborn usó en K1-K3
KW = {
  "KRYPTOS": (2,0,5,1,3,4,6),
  "PALIMPSEST": (1,0,5,6,3,2,8,4,7,9), # truncamos a 7
  "BERLIN": (2,1,4,0,3,5),
  "BERLINCLOCK": (2,1,4,0,3,5,1,6,7,3,2),
  "CLOCK": (1,3,0,2,4)
}

def uncolumnar(text, perm):
    k=len(perm)
    n=len(text)
    rows=math.ceil(n/k)
    col_lens=[rows]*k
    rem=rows*k-n
    for i in range(rem):
        # ultima columna en orden de escritura es mas corta - asumimos pad izquierda
        col_lens[k-1-i]-=1
    cols=['']*k
    idx=0
    order=sorted(range(k), key=lambda x: perm[x])
    for c in order:
        l=col_lens[c]
        cols[c]=text[idx:idx+l]
        idx+=l
    out=[]
    for r in range(rows):
        for c in range(k):
            if r < len(cols[c]):
                out.append(cols[c][r])
    return ''.join(out)

class DoubleColumnarBeaufortEngine(BaseCryptoEngine):
    @property
    def name(self): return "DoubleColumnarBeaufort"

    def decrypt(self, ct, key):
        perm1, perm2, bkey = key
        # 1. undo col2
        t1 = uncolumnar(ct, perm2)
        # 2. undo col1
        t2 = uncolumnar(t1, perm1)
        # 3. Beaufort decrypt: Pt = (Kt - Ct) mod 26
        res=[]
        for i,ch in enumerate(t2):
            c=ord(ch)-65
            k=ord(bkey[i % len(bkey)])-65
            p=(k - c) % 26
            res.append(chr(p+65))
        return ''.join(res)

    def get_key_generator(self):
        # Doble columnar 6 y 7 es enorme, probamos combos reales de KRYPTOS/PALIMPSEST
        perms6 = [(2,0,5,1,3,4),(1,0,5,6,3,2)] # KRYPTOS6, PALIMPSEST6
        perms7 = [(2,0,5,1,3,4,6)] # KRYPTOS7
        bkeys = ["BERLIN","CLOCK","BERLINCLOCK","KRYPTOS","SOTPYRK","NORTHEAST"]
        for p1 in perms6:
            for p2 in perms7:
                for bk in bkeys:
                    yield (p1,p2,bk)
                    yield (p2,p1,bk) # orden inverso

