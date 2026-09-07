from itertools import permutations
from src.core.base_engine import BaseCryptoEngine
import math

class HillMatrix2x2(BaseCryptoEngine):
    @property
    def name(self): return "HillMatrix3x3-Neon"

    def get_key_generator(self, **kwargs):
        digits = list(range(9))
        # matriz madre 0-8
        base = [[0,1,2],[3,4,5],[6,7,8]]
        # prueba todas las permutaciones de 0-8 como 3x3
        seen=set()
        for perm in permutations(digits, 9):
            if perm[:3]==(0,1,2) and perm[3:6]==(3,4,5): # evita repetir base demasiadas
                pass
            m = [list(perm[0:3]), list(perm[3:6]), list(perm[6:9])]
            # det mod26 rápido
            det = (m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1]) - m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0]) + m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0])) % 26
            if det==0 or math.gcd(det,26)!=1: continue
            key=tuple(perm)
            if key in seen: continue
            seen.add(key)
            yield m
            if len(seen)>5000: break # cap para no explotar - 5k keys

    def decrypt(self,ciphertext,key):
        alpha="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        # inversa 3x3 mod26
        m=key
        det = (m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1]) - m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0]) + m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0])) %26
        inv_det=pow(det,-1,26)
        # adjunta
        adj=[
            [(m[1][1]*m[2][2]-m[1][2]*m[2][1]), -(m[0][1]*m[2][2]-m[0][2]*m[2][1]), (m[0][1]*m[1][2]-m[0][2]*m[1][1])],
            [-(m[1][0]*m[2][2]-m[1][2]*m[2][0]), (m[0][0]*m[2][2]-m[0][2]*m[2][0]), -(m[0][0]*m[1][2]-m[0][2]*m[1][0])],
            [(m[1][0]*m[2][1]-m[1][1]*m[2][0]), -(m[0][0]*m[2][1]-m[0][1]*m[2][0]), (m[0][0]*m[1][1]-m[0][1]*m[1][0])]
        ]
        inv=[[ (adj[i][j]*inv_det)%26 for j in range(3)] for i in range(3)]
        pt=""
        for i in range(0,len(ciphertext),3):
            chunk=ciphertext[i:i+3]
            if len(chunk)<3: chunk+="XX"
            v=[alpha.index(c) if c in alpha else 0 for c in chunk]
            p=[(inv[0][0]*v[0]+inv[0][1]*v[1]+inv[0][2]*v[2])%26,
               (inv[1][0]*v[0]+inv[1][1]*v[1]+inv[1][2]*v[2])%26,
               (inv[2][0]*v[0]+inv[2][1]*v[1]+inv[2][2]*v[2])%26]
            pt+="".join(alpha[x] for x in p)
        return pt[:97]

HillMatrixEngine=HillMatrix2x2
