from PIL import Image
import os

K4 = "OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
A="ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def modinv(a,m=26):
    for x in range(m):
        if (a*x)%m==1: return x
    return None

# Hill 0.png [[3,3],[2,5]] -> inv
m0=[[3,3],[2,5]]
det=(m0[0][0]*m0[1][1]-m0[0][1]*m0[1][0])%26
di=modinv(det)
print(f"Hill0 det={det} inv={di}")
inv=[[m0[1][1]*di %26, -m0[0][1]*di %26],[ -m0[1][0]*di %26, m0[0][0]*di %26]]
inv=[[x%26 for x in r] for r in inv]
print(f"Hill0 inv={inv}")

# Berlin bits -> estado reloj?
b4=list(Image.open("assets/4.png").getdata())
b4=[1 if p==255 else 0 for p in b4]
b5=list(Image.open("assets/5.png").getdata())
b5=[1 if p==255 else 0 for p in b5]
print(f"Berlin byte0 {b4} = {int(''.join(map(str,b4)),2)}")
print(f"Berlin byte1 {b5} = {int(''.join(map(str,b5)),2)}")

# LFSR
taps=list(Image.open("assets/7.png").getdata())
taps=[1 if p==255 else 0 for p in taps]
print(f"LFSR taps {taps}")

# Tableau 8.png
tab=Image.new("L",(26,26))
tab=list(Image.open("assets/8.png").getdata())
print(f"Tableau 26x26 OK len={len(tab)}")

# Decrypt simple: Hill -> luego BERLIN EAST/NORTHEAST crib
def hill_decrypt(txt, inv):
    out=""
    for i in range(0,len(txt),2):
        v1=A.index(txt[i]); v2=A.index(txt[i+1]) if i+1<len(txt) else 0
        d1=(inv[0][0]*v1+inv[0][1]*v2)%26
        d2=(inv[1][0]*v1+inv[1][1]*v2)%26
        out+=A[d1]+A[d2]
    return out

plain=hill_decrypt(K4, inv)
print("\n[K4 Hill decrypted]:\n",plain[:100])
# Crib search BERLIN
for i in range(len(plain)-5):
    if "BERLIN" in plain[i:i+6] or "EAST" in plain[i:i+6]:
        print(f"FOUND {plain[i:i+20]} at {i}")

