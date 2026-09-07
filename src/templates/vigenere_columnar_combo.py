from itertools import permutations, product
from src.core.base_engine import BaseCryptoEngine
import math

class VigenereColumnarComboEngine(BaseCryptoEngine):
    @property
    def name(self): return "VigenereColumnarCombo"

    def get_key_generator(self, **kwargs):
        # keywords Kryptos: KRYPTOS, PALIMPSEST, ABSCISSA, BERLIN, CLOCK
        base_words = ["KRYPTOS","PALIMPSEST","ABSCISSA","BERLIN","CLOCK","BERLINCLOCK"]
        col_keys = []
        for k in [4,5,6,7]:
            for p in permutations(list(range(k))):
                col_keys.append(p)
        for word in base_words:
            # variaciones cortas de la keyword vigenere
            for w in [word, word[:4], word[:5], word[::-1]]:
                for ck in col_keys:
                    yield (w, ck)

    def decrypt(self, ciphertext, key):
        vig_key, col_key = key
        alpha="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        # 1. invierte columnar
        k=len(col_key)
        n=len(ciphertext)
        rows=math.ceil(n/k)
        order=sorted(range(k), key=lambda x: col_key[x])
        grid=[['']*k for _ in range(rows)]
        pos=0
        for c in order:
            for r in range(rows):
                if pos<n:
                    grid[r][c]=ciphertext[pos]
                    pos+=1
        step1="".join("".join(row) for row in grid)[:n]
        # 2. vigenere decrypt
        pt=""
        for i,ch in enumerate(step1):
            if ch not in alpha: continue
            kv=alpha.index(vig_key[i % len(vig_key)])
            cv=alpha.index(ch)
            pt+=alpha[(cv - kv) % 26]
        return pt
