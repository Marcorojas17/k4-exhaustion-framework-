from PIL import Image
K4="OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
A="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
def a2i(c): return A.index(c)
def i2a(i): return A[i%26]

# 2.png y 3.png = claves columnar
def get_col_order(path):
    data=list(Image.open(path).get_flattened_data() if hasattr(Image.open(path),'get_flattened_data') else Image.open(path).getdata())
    # data es 0-25 repetido, usamos como orden
    return data

# Berlin bytes
b4=[1 if p==255 else 0 for p in Image.open("assets/4.png").getdata()]
b5=[1 if p==255 else 0 for p in Image.open("assets/5.png").getdata()]
berlin_time = int(''.join(map(str,b4+b5)),2) % 1440 # minutos del dia
print(f"Berlin combined {b4+b5} -> {berlin_time} min = {berlin_time//60:02d}:{berlin_time%60:02d}")

# LFSR keystream desde taps 0,1,3,4
taps=[0,1,3,4]
state = (1<<24)-1
keystream=[]
for _ in range(len(K4)):
    fb=0
    for t in taps: fb ^= (state>>t) & 1
    state = ((state<<1) & 0xFFFFFF) | fb
    keystream.append(state & 0x1F)

print(f"LFSR keystream first 20: {keystream[:20]}")

# Brute: K4 - keystream + Vigenere tableau 8.png (r+c)%26 => plain = (cipher - ks - tableau_row) mod26
for shift in range(26):
    plain=""
    for i,ch in enumerate(K4):
        c=a2i(ch)
        k=keystream[i] %26
        p=(c - k - shift) %26
        plain+=i2a(p)
    if "BERLIN" in plain or "CLOCK" in plain or "EAST" in plain or "NORTHEAST" in plain:
        print(f"*** HIT shift={shift} : {plain}")

# Tambien prueba crib BERLIN CLOCK como en Kryptos docs
# Si no sale, prueba Hill inv despues de quitar LFSR
m_inv=[[15,17],[20,9]]
def hill_dec(txt):
    out=""
    for i in range(0,len(txt),2):
        if i+1>=len(txt): break
        v1=a2i(txt[i]); v2=a2i(txt[i+1])
        out+=i2a((m_inv[0][0]*v1+m_inv[0][1]*v2)%26)
        out+=i2a((m_inv[1][0]*v1+m_inv[1][1]*v2)%26)
    return out

for shift in range(26):
    # paso 1: quitar lfsr
    step1="".join(i2a((a2i(c)-keystream[i])%26) for i,c in enumerate(K4))
    step2=hill_dec(step1)
    if "BERLIN" in step2:
        print(f"HILL+LFSR HIT shift {shift}: {step2}")

print("[*] Si no hay HIT, siguiente es probar columnar con 2.png (4x25)")
# Columnar 4x25: K4 97 chars -> matrix 4 rows x 25 cols
def col_decrypt(txt, cols=25):
    rows=4
    # rellena por columnas con orden i%26
    order=list(range(cols))
    # orden simple: 0..24
    # transposición: escribe por columnas, lee por filas
    matrix=['']*rows
    idx=0
    for c in order:
        for r in range(rows):
            if idx < len(txt):
                if len(matrix[r]) <= c:
                    matrix[r] = matrix[r].ljust(c+1)
                # simplificado
                pass
    return txt

