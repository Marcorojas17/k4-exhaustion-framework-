from itertools import permutations
from src.core.base_engine import BaseCryptoEngine
import math

class HillMatrixEngine(BaseCryptoEngine):
    @property
    def name(self): return "HillMatrix2x2"
    def get_key_generator(self, **kwargs):
        digits=list(range(9))
        seen=set()
        for a,b,c,d in permutations(digits,4):
            det=(a*d-b*c)%26
            if det==0 or math.gcd(det,26)!=1: continue
            if (a,b,c,d) in seen: continue
            seen.add((a,b,c,d))
            yield [[a,b],[c,d]]
    def decrypt(self,ciphertext,key):
        alpha="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        a,b=key[0]; c,d=key[1]
        det=(a*d-b*c)%26
        inv_det=pow(det,-1,26)
        inv=[[(d*inv_det)%26, (-b*inv_det)%26],[(-c*inv_det)%26,(a*inv_det)%26]]
        pt=""
        for i in range(0,len(ciphertext),2):
            pair=ciphertext[i:i+2]
            if len(pair)<2: pair+="X"
            v0=alpha.index(pair[0]); v1=alpha.index(pair[1])
            p0=(inv[0][0]*v0+inv[0][1]*v1)%26
            p1=(inv[1][0]*v0+inv[1][1]*v1)%26
            pt+=alpha[p0]+alpha[p1]
        return pt
