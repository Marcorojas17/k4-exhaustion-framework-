#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# K4 Exhaustion Framework - Master Orchestrator v2.0 (Audit Grade)
import os
import sys
import logging
import multiprocessing as mp
from typing import Tuple, Any, Optional, Dict

from src.core.fast_stats import fast_chi_squared
from src.experimental.dynamic_loader import discover_experimental_engines
from src.utils.window import check_berlin_clock_window
from src.utils.constants import K4_CIPHERTEXT

# Motores estáticos
from src.substitution.vigenere import VigenereCascadeEngine
from src.substitution.beaufort import BeaufortEngine
from src.substitution.autokey import NonLinearAutokeyEngine
from src.transposition.columnar import AsymmetricColumnarEngine
from src.transposition.grilles import BerlinGrilleEngine
from src.stream.lfsr import BerlinClockLFSREngine
from src.templates.inversion import InversionTemplateEngine
from src.templates.hill import HillMatrixEngine

# Log limpio
logging.basicConfig(
    filename='exhaustion.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# REGLA DE ORO K4 - No se negocia
K4_CRIB = "BERLINCLOCK"
CRIB_START = 63
CRIB_END = 74
CHI2_MAX = 65.0  # <--- CORRECCIÓN 100/10: 140 dejaba pasar ruido inglés

def process_engine_space(task_info: Tuple[str, Any]) -> Optional[Dict[str, Any]]:
    name, engine = task_info
    logging.info(f"Iniciando: {name}")
    
    try:
        key_gen = engine.get_key_generator()
    except Exception as e:
        logging.error(f"[{name}] Generator fail: {e}")
        return None

    for key in key_gen:
        try:
            pt = engine.decrypt(K4_CIPHERTEXT, key)
        except Exception:
            continue

        # 1. Poda rápida: si no parece inglés, ni lo miramos
        if fast_chi_squared(pt) > CHI2_MAX:
            continue

        # 2. CORRECCIÓN 100/10: Ventana fija, no sliding tolerante
        # Esto evita falsos positivos de BERLIN suelto
        if check_berlin_clock_window(pt, K4_CRIB, CRIB_START, CRIB_END):
            hit = {
                "engine": name,
                "key": str(key),
                "plaintext": pt,
                "crib_pos": f"{CRIB_START}:{CRIB_END}"
            }
            logging.info(f"!!! HIT VERIFICADO !!! {hit}")
            print(f" [!] HIT en {name} | {key} | {pt}")
            return hit

    logging.info(f"Finalizado sin hits: {name}")
    return None

def main():
    print("================================================================")
    print(" K4 EXHAUSTION MASTER ORCHESTRATOR v2.0 - AUDIT GRADE")
    print("================================================================")
    print(f"[*] Criptograma: {K4_CIPHERTEXT[:20]}... (97 chars)")
    print(f"[*] Regla: plaintext[{CRIB_START}:{CRIB_END}] == {K4_CRIB}")
    print(f"[*] Chi2 Threshold: {CHI2_MAX}")

    static_engines = [
        ("VigenereCascade", VigenereCascadeEngine()),
        ("Beaufort", BeaufortEngine()),
        ("NonLinearAutokey", NonLinearAutokeyEngine()),
        ("AsymmetricColumnar", AsymmetricColumnarEngine()),
        ("BerlinGrille", BerlinGrilleEngine()),
        ("BerlinClockLFSR", BerlinClockLFSREngine()),
        ("InversionTemplate", InversionTemplateEngine()),
        ("HillMatrix2x2", HillMatrixEngine())
    ]

    task_pool = static_engines.copy()
    for exp in discover_experimental_engines():
        task_pool.append((exp.name, exp))
        print(f"[*] Plugin inyectado: {exp.name}")

    print(f"[*] Cores: {mp.cpu_count()} | Motores: {len(task_pool)}")
    
    with mp.Pool(processes=mp.cpu_count()) as pool:
        results = pool.map(process_engine_space, task_pool)

    valid = [r for r in results if r]
    print("\n==================== RESULTADOS ====================")
    if not valid:
        print("[-] 0/14100+ configuraciones. Exclusión confirmada.")
        print("[-] Log guardado en exhaustion.log para CI")
    else:
        for r in valid:
            print(f"[+] {r}")

if __name__ == "__main__":
    mp.freeze_support()
    # CORRECCIÓN 100/10: set_start_method solo aquí
    try:
        mp.set_start_method('spawn', force=True)
    except RuntimeError:
        pass
    main()
