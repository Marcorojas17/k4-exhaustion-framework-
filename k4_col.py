import numpy as np

K4 = "OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
KRYPTOS_ALPHABET = "KRYPTOSABCDEFGHIJLMNQUVWXZ"

k4_numeric = np.array([KRYPTOS_ALPHABET.index(c) for c in K4], dtype=np.int32)

def run_lfsr_vectorized(seed_24bit, length=97):
    taps = [0, 1, 3, 4]
    state = seed_24bit if seed_24bit != 0 else 1
    ks = np.zeros(length, dtype=np.int32)
    for i in range(length):
        fb = 0
        for t in taps:
            fb ^= (state >> t) & 1
        state = ((state << 1) & 0xFFFFFF) | fb
        ks[i] = state % 26
    return ks

def col_unshuffle_numpy(arr_numeric, rows=4, cols=25):
    m = np.zeros((rows, cols), dtype=np.int32)
    idx = 0
    for c in range(cols):
        for r in range(rows):
            if idx < len(arr_numeric):
                m[r, c] = arr_numeric[idx]
                idx += 1
    return m.flatten()[:len(arr_numeric)]

print("[*] Des-transponiendo K4 de forma vectorial...")
k4_row_major = col_unshuffle_numpy(k4_numeric, 4, 25)

print("[*] Lanzando escáner sobre el Alfabeto Modificado KRYPTOS...")
hits = 0

berlin_vec = np.array([KRYPTOS_ALPHABET.index(c) for c in "BERLIN"], dtype=np.int32)
clock_vec = np.array([KRYPTOS_ALPHABET.index(c) for c in "CLOCK"], dtype=np.int32)

all_shifts = np.arange(26, dtype=np.int32).reshape(26, 1)

for h in range(24):
    for m in range(60):
        b1 = (1 << (h // 5)) - 1 if h // 5 > 0 else 0
        b2 = (1 << (h % 5)) - 1 if h % 5 > 0 else 0
        b3 = (1 << (m // 5)) - 1 if m // 5 > 0 else 0
        b4 = (1 << (m % 5)) - 1 if m % 5 > 0 else 0
        
        seed = (b1 << 16) | (b2 << 12) | (b3 << 4) | b4
        ks = run_lfsr_vectorized(seed, len(k4_row_major))
        base_decrypted = (k4_row_major - ks) % 26
        matrix_decrypted = (base_decrypted - all_shifts) % 26
        
        for shift in range(26):
            row_text = matrix_decrypted[shift]
            
            for pos in range(len(row_text) - 5):
                window = row_text[pos:pos+6]
                if np.sum(window == berlin_vec) >= 5:
                    text_str = "".join([KRYPTOS_ALPHABET[idx] for idx in row_text])
                    print(f" [★] EXCELENTE HIT -> Time [{h:02d}:{m:02d}] Shift={shift} Pos={pos} (BERLIN)")
                    print(f"     Texto: {text_str[:pos]}>>{text_str[pos:pos+6]}<<{text_str[pos+6:pos+40]}...\n")
                    hits += 1

            for pos in range(len(row_text) - 4):
                window = row_text[pos:pos+5]
                if np.sum(window == clock_vec) >= 5:
                    text_str = "".join([KRYPTOS_ALPHABET[idx] for idx in row_text])
                    print(f" [★] EXCELENTE HIT -> Time [{h:02d}:{m:02d}] Shift={shift} Pos={pos} (CLOCK)")
                    print(f"     Texto: {text_str[:pos]}>>{text_str[pos:pos+5]}<<{text_str[pos+5:pos+40]}...\n")
                    hits += 1

print(f"[+] Escaneo en alfabeto Kryptos concluido. Candidatos perfectos: {hits}")
