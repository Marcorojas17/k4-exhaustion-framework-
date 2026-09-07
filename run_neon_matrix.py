#!/usr/bin/env python3
import os
import pathlib
import numpy as np
from PIL import Image

K4 = "OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
KRYPTOS_ALPHABET = "KRYPTOSABCDEFGHIJLMNQUVWXZ"

k4_numeric = np.array([KRYPTOS_ALPHABET.index(c) for c in K4], dtype=np.int32)
berlin_vec = np.array([KRYPTOS_ALPHABET.index(c) for c in "BERLIN"], dtype=np.int32)
clock_vec = np.array([KRYPTOS_ALPHABET.index(c) for c in "CLOCK"], dtype=np.int32)

def extract_matrix_from_png(path):
    if not os.path.exists(path):
        return [0, 0, 0, 0]
    img = Image.open(path).convert("RGB")
    arr = np.array(img)
    r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
    
    magenta_mask = (r > 180) & (b > 120) & (g < 120)
    cyan_mask = (g > 120) & (b > 120) & (r < 120)
    
    h, w = r.shape
    quadrants = [
        (slice(0, h//2), slice(0, w//2)),
        (slice(0, h//2), slice(w//2, w)),
        (slice(h//2, h), slice(0, w//2)),
        (slice(h//2, h), slice(w//2, w))
    ]
    vals = []
    for rs, cs in quadrants:
        m_count = np.sum(magenta_mask[rs, cs])
        c_count = np.sum(cyan_mask[rs, cs])
        vals.append(1 if m_count > c_count else 0)
    
    if vals ==: vals = [1, 0, 0, 1]
    if vals ==: vals = [1, 0, 1, 0]
    return vals

def col_unshuffle_numpy(arr_numeric, rows=4, cols=25):
    m = np.zeros((rows, cols), dtype=np.int32)
    idx = 0
    for c in range(cols):
        for r in range(rows):
            if idx < len(arr_numeric):
                m[r, c] = arr_numeric[idx]
                idx += 1
    return m.flatten()[:len(arr_numeric)]

def main():
    print("[*] Leyendo e interpretando las 9 Rejillas de Neón...")
    assets_dir = "assets"
    raw_bits = []
    
    for i in range(9):
        p = pathlib.Path(assets_dir) / f"{i}.png"
        bits = extract_matrix_from_png(str(p))
        raw_bits.extend(bits)
        print(f"  -> {i}.png interpretado binario: {bits}")
        
    keystream = np.array([b % 26 for b in raw_bits * 3], dtype=np.int32)[:len(K4)]
    
    print("[*] Des-transponiendo K4 (Cuadrícula Estructural 4x25)...")
    k4_row_major = col_unshuffle_numpy(k4_numeric, 4, 25)
    
    print("[*] Probando todos los estados del Berlin Clock + Shifts César...")
    all_shifts = np.arange(26, dtype=np.int32).reshape(26, 1)
    hits = 0
    
    for h in range(24):
        for m in range(60):
            b1 = (1 << (h // 5)) - 1 if h // 5 > 0 else 0
            b2 = (1 << (h % 5)) - 1 if h % 5 > 0 else 0
            b3 = (1 << (m // 5)) - 1 if m // 5 > 0 else 0
            b4 = (1 << (m % 5)) - 1 if m % 5 > 0 else 0
            clock_seed = (b1 << 16) | (b2 << 12) | (b3 << 4) | b4
            
            dynamic_ks = (keystream + clock_seed) % 26
            base_decrypted = (k4_row_major - dynamic_ks) % 26
            matrix_decrypted = (base_decrypted - all_shifts) % 26
            
            for shift in range(26):
                row_text = matrix_decrypted[shift]
                
                for pos in range(len(row_text) - 5):
                    window = row_text[pos:pos+6]
                    if np.sum(window == berlin_vec) >= 4:
                        text_str = "".join([KRYPTOS_ALPHABET[idx] for idx in row_text])
                        print(f" [!] HIT NEÓN -> [{h:02d}:{m:02d}] Shift={shift} Pos={pos} (BERLIN)")
                        print(f"     Texto: {text_str[:pos]}>>{text_str[pos:pos+6]}<<{text_str[pos+6:pos+40]}...\n")
                        hits += 1

                for pos in range(len(row_text) - 4):
                    window = row_text[pos:pos+5]
                    if np.sum(window == clock_vec) >= 4:
                        text_str = "".join([KRYPTOS_ALPHABET[idx] for idx in row_text])
                        print(f" [!] HIT NEÓN -> [{h:02d}:{m:02d}] Shift={shift} Pos={pos} (CLOCK)")
                        print(f"     Texto: {text_str[:pos]}>>{text_str[pos:pos+5]}<<{text_str[pos+5:pos+40]}...\n")
                        hits += 1

    print(f"[+] Análisis masivo concluido. Candidatos extraídos de la Neon Matrix: {hits}")

if __name__ == "__main__":
    main()
