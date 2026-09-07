#!/usr/bin/env python3
# ==============================================================================
# KRONOS CRYPTOANALYTICAL MATRIX ENGINE v13.9 - K4 DICTIONARY FILTER
# MATRICES BILINGÜES, CONTEO DE N-GRAMAS Y FILTRADO POR CLAVES HISTÓRICAS
# AUTORÍA REGISTRADA: DIRECTOR MARCO ANTONIO ROJAS VALDOVINOS (TOLUCA DE LERDO)
# ==============================================================================

import itertools
import sys
import collections

# Criptograma de 97 caracteres de K4 (Kryptos)
K4_CIPHERTEXT = "OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOOTWTQSSESTXOCDTJDUTGRIJWTLBTCXSAESBBICFWXASBIZFBRAZEUWIGKFIZ"

TOP_ENGLISH_BIGRAMS = ["TH", "HE", "IN", "ER", "AN", "RE", "ED", "ON", "ES", "ST"]
TOP_ENGLISH_TRIGRAMS = ["THE", "AND", "THA", "ENT", "ING", "ION", "TIO", "FOR", "NDE", "HAS"]
TOP_SPANISH_BIGRAMS = ["DE", "ES", "EN", "EL", "RE", "LA", "ON", "AS", "DE", "OS"]
TOP_SPANISH_TRIGRAMS = ["DEL", "QUE", "EST", "ENT", "LOS", "COM", "CON", "LAS", "PAR", "RES"]

# Diccionario histórico oficial de pistas reveladas por Sanborn/CIA para K4
KRYPTOS_TARGET_WORDS = ["PALIMPSEST", "BERLIN", "NORTHEAST", "CLOCK"]

def matrix_transpose_permutation(text, key_permutation):
    num_columns = len(key_permutation)
    num_rows = (len(text) + num_columns - 1) // num_columns
    padded_text = text.ljust(num_columns * num_rows, '?')
    grid = [padded_text[i:i+num_columns] for i in range(0, len(padded_text), num_columns)]
    decrypted_blocks = []
    for row in grid:
        reordered_row = "".join(row[p] for p in key_permutation if p < len(row))
        decrypted_blocks.append(reordered_row)
    return "".join(decrypted_blocks)

def apply_modular_vigenere_mod26(ciphertext, key):
    decrypted = []
    key_length = len(key)
    for i, char in enumerate(ciphertext):
        if char.isalpha():
            c_val = ord(char) - 65
            k_val = ord(key[i % key_length].upper()) - 65
            p_val = (c_val - k_val) % 26
            decrypted.append(chr(p_val + 65))
        else:
            decrypted.append(char)
    return "".join(decrypted)

def analyze_bilingual_frequency_with_dict(text):
    bigrams = [text[i:i+2] for i in range(len(text)-1) if "?" not in text[i:i+2]]
    trigrams = [text[i:i+3] for i in range(len(text)-2) if "?" not in text[i:i+3]]
    b_counts = collections.Counter(bigrams)
    t_counts = collections.Counter(trigrams)
    
    score = 0
    for bg in TOP_ENGLISH_BIGRAMS + TOP_SPANISH_BIGRAMS:
        score += b_counts[bg] * 2
    for tg in TOP_ENGLISH_TRIGRAMS + TOP_SPANISH_TRIGRAMS:
        score += t_counts[tg] * 5
        
    # Inyección del Filtro de Diccionario de la CIA
    for word in KRYPTOS_TARGET_WORDS:
        if word in text:
            score += 50 # Bonificación masiva por colisión temática exacta
            
    return score

def execute_exhaustion_pipeline(sample_depth=10):
    print(f"\033[0;36m[K4_ENGINE v13.9] Inicializando análisis espectral bilingüe con diccionario...\033[0;0m")
    base_indices = list(range(4))
    permutations = list(itertools.permutations(base_indices))
    
    candidates_found = []
    count = 0
    print("----------------------------------------------------------------------")
    for perm in permutations[:sample_depth]:
        count += 1
        transposed = matrix_transpose_permutation(K4_CIPHERTEXT, perm)
        candidate = apply_modular_vigenere_mod26(transposed, "BERLIN")
        score = analyze_bilingual_frequency_with_dict(candidate)
        
        if score > 0:
            candidates_found.append((score, perm, candidate))
            
        bar = "█" * min(score, 50) # Limitar la barra visual por estética
        print(f"\033[1;37mArr #{count} {perm}\033[0;0m [Score {score:2d}]: {bar}")
    
    if candidates_found:
        candidates_found.sort(reverse=True, key=lambda x: x)
        with open("candidates.txt", "w") as cf:
            cf.write("=== REPORTE DE CANDIDATOS FILTRADOS K4 (KRONOS v13.9) ===\n")
            for score, perm, cand in candidates_found:
                cf.write(f"Score: {score} | Permutación: {perm} | Texto: {cand}\n")
        print("----------------------------------------------------------------------")
        print("\033[0;32m[REGISTRO]\033[0;0m Datos actualizados en la raíz: candidates.txt")
    print("\033[0;32m[SUCCESS]\033[0;0m Criptoanálisis bilingüe con filtro semántico completado.")

if __name__ == "__main__":
    execute_exhaustion_pipeline()
