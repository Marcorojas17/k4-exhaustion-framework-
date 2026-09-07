from PIL import Image
K4="OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
A="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
a2i=lambda c: A.index(c)
i2a=lambda i: A[i%26]

# 01:44 -> key = 1+44=45 -> 45%26=19 = T
berlin_hour, berlin_min = 1,44
key_shift = (berlin_hour*60 + berlin_min) % 26
print(f"BERLIN KEY SHIFT from 01:44 = {key_shift} -> {i2a(key_shift)}")

# LFSR
taps=[0,1,3,4]
state=(1<<24)-1
ks=[]
for _ in range(len(K4)):
    fb=0
    for t in taps: fb ^= (state>>t) & 1
    state = ((state<<1) & 0xFFFFFF) | fb
    ks.append(state % 26)

def hill_inv_decrypt(txt):
    inv=[[15,17],[20,9]]
    out=""
    for i in range(0,len(txt)-1,2):
        v1=a2i(txt[i]); v2=a2i(txt[i+1])
        out+=i2a((inv[0][0]*v1+inv[0][1]*v2)%26)
        out+=i2a((inv[1][0]*v1+inv[1][1]*v2)%26)
    if len(txt)%2==1: out+=txt[-1]
    return out

# Prueba final con crib EAST NORTH EAST
cribs=["BERLIN","CLOCK","EAST","NORTHEAST","BERLINCLOCK"]
best=[]
for k_shift in [key_shift] + list(range(26)):
    # paso LFSR
    s1="".join(i2a((a2i(c)-ks[i])%26) for i,c in enumerate(K4))
    s1="".join(i2a((a2i(c)-ks[i]-k_shift)%26) for i,c in enumerate(K4))
    s2=hill_inv_decrypt(s1)
    for crib in cribs:
        if crib in s2:
            best.append((k_shift,s2))
            print(f"HIT {crib} shift={k_shift}: {s2}")

if not best:
    print("No BERLIN en Hill+LFSR, probando raw LFSR + Vigenere 8.png")
    for k_shift in range(26):
        s1="".join(i2a((a2i(c)-ks[i]-k_shift)%26) for i,c in enumerate(K4))
        print(f"shift {k_shift}: {s1[:80]}")

print("\nGuardando candidatos en candidates.txt")
open("candidates.txt","w").write("\n".join([b[1] for b in best]))
