from itertools import permutations
from src.core.base_engine import BaseCryptoEngine
import math

class HillColumnarComboEngine(BaseCryptoEngine):
    @property
    def name(self): return "HillColumnarCombo"
    def get_key_generator(self, **kwargs):
        col_keys=[]
        for k in [3,4,5]:
            for p in permutations(list(range(k))):
                col_keys.append(p)
        hill=[]
        for perm in permutations(list(range(9)),9):
            m=[list(perm[0:3]), list(perm[3:6]), list(perm[6:9])]
            det=(m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1]) - m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0]) + m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]))%26
            if det==0 or math.gcd(det,26)!=1: continue
            hill.append(m)
            if len(hill)>=200: break
        for ck in col_keys:
            for hk in hill:
                yield (ck, hk)
    def decrypt(self, ciphertext, key):
        col_key, hill_key = key
        alpha="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
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
        m=hill_key
        det=(m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1]) - m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0]) + m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]))%26
        inv_det=pow(det,-1,26)
        adj=[[(m[1][1]*m[2][2]-m[1][2]*m[2][1]), -(m[0][1]*m[2][2]-m[0][2]*m[2][1]), (m[0][1]*m[1][2]-m[0][2]*m[1][1])],[-(m[1][0]*m[2][2]-m[1][2]*m[2][0]), (m[0][0]*m[2][2]-m[0][2]*m[2][0]), -(m[0][0]*m[1][2]-m[0][2]*m[1][0])],[(m[1][0]*m[2][1]-m[1][1]*m[2][0]), -(m[0][0]*m[2][1]-m[0][1]*m[2][0]), (m[0][0]*m[1][1]-m[0][1]*m[1][0])]]
        inv=[[(adj[i][j]*inv_det)%26 for j in range(3)] for i in range(3)]
        clean=[c for c in step1 if c in alpha]
        if len(clean)%3!=0: clean+=['X']*(3-len(clean)%3)
        pt=""
        for i in range(0,len(clean),3):
            v=[alpha.index(clean[i+j]) for j in range(3)]
            p=[(inv[r][0]*v[0]+inv[r][1]*v[1]+inv[r][2]*v[2])%26 for r in range(3)]
            pt+="".join(alpha[x] for x in p)
        return pt[:n]
