from src.core.base_engine import BaseCryptoEngine

# Berlin Clock real: 4 filas
# Row1: 5h *4 (rojo)
# Row2: 1h *4 (rojo)
# Row3: 5m *11 (3 amarillo/rojo)
# Row4: 1m *4 (amarillo)
def berlin_clock_state(h,m):
    # retorna lista de 23 bits (luces prendidas)
    row1 = [1 if (h//5) > i else 0 for i in range(4)]
    row2 = [1 if (h%5) > i else 0 for i in range(4)]
    row3 = [1 if (m//5) > i else 0 for i in range(11)]
    row4 = [1 if (m%5) > i else 0 for i in range(4)]
    return row1+row2+row3+row4 # 23 bits

def lfsr_keystream(seed_bits, length):
    # LFSR simple de 23 bits, polinomio x23 + x5 +1 (estandar)
    state = seed_bits[:]
    out=[]
    for _ in range(length):
        out.append(state[-1])
        # feedback
        fb = state[0] ^ state[4] # taps 23 y 5
        state = [fb] + state[:-1]
    return out

class BerlinClockLFSRRealEngine(BaseCryptoEngine):
    @property
    def name(self): return "BerlinClockLFSRReal"
    def decrypt(self, ct, key):
        h,m,method = key
        seed = berlin_clock_state(h,m)
        ks_bits = lfsr_keystream(seed, len(ct)*5) # 5 bits por letra
        # convertir bits a shifts 0-25
        shifts=[]
        for i in range(len(ct)):
            b = ks_bits[i*5:(i+1)*5]
            val = (b[0]*16 + b[1]*8 + b[2]*4 + b[3]*2 + b[4]) % 26
            shifts.append(val)
        res=[]
        for i,ch in enumerate(ct):
            c=ord(ch)-65
            if method=="sub":
                p=(c - shifts[i]) % 26
            else: # beaufort
                p=(shifts[i] - c) % 26
            res.append(chr(p+65))
        return ''.join(res)

    def get_key_generator(self):
        # Probamos cada hora del día, minutos 0,15,30,45
        for h in range(24):
            for m in [0,15,30,45]:
                for method in ["sub","beaufort"]:
                    yield (h,m,method)

