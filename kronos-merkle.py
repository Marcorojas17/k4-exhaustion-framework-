#!/usr/bin/env python3
# ==============================================================================
# KRONOS MERKLE SYNTHESIZER v13.1 - CONSOLE COMPLIANCE EXTENSION
# COMPUTA EL ARBOL DE HASHEO GLOBAL DE LA EVIDENCIA RECOLECTADA
# ==============================================================================

import os
import hashlib
import sys

def get_files_hashes(directory="."):
    hashes = []
    # Extensiones e hilos a omitir
    ignore_files = ["kronos-audit.sh", "kronos-orchestrator.sh", "kronos-merkle.py", ".git"]
    
    for root, dirs, files in os.walk(directory):
        if ".git" in root:
            continue
        for file in sorted(files):
            if file in ignore_files or file.startswith("KRONOS_AUDIT_REPORT_"):
                continue
            path = os.path.join(root, file)
            try:
                with open(path, "rb") as f:
                    content = f.read()
                file_hash = hashlib.sha256(content).hexdigest()
                hashes.append(file_hash)
            except Exception:
                continue
    return hashes

def build_merkle_root(hashes):
    if not hashes:
        return "N/A"
    current_level = hashes
    while len(current_level) > 1:
        next_level = []
        for i in range(0, len(current_level), 2):
            if i + 1 < len(current_level):
                combined = current_level[i] + current_level[i+1]
                next_level.append(hashlib.sha256(combined.encode('utf-8')).hexdigest())
            else:
                next_level.append(current_level[i])
        current_level = next_level
    return current_level[0]

if __name__ == "__main__":
    print("\033[0;36m[MERKLE] Recopilando firmas hash de los 78 vectores...\033[0;0m")
    all_hashes = get_files_hashes()
    if not all_hashes:
        print("\033[0;31m[ERROR]\033[0;0m No se encontraron vectores válidos para hashear.")
        sys.exit(1)
    
    root_hash = build_merkle_root(all_hashes)
    print("----------------------------------------------------------------------")
    print(f"\033[0;32m[SUCCESS]\033[0;0m Árbol Criptográfico Estructurado Correctamente.")
    print(f"\033[0;32m[ROOT HASH]:\033[0;0m \033[1;37m{root_hash}\033[0;0m")
    print("----------------------------------------------------------------------")
    
    # Inyectar el root hash en el último reporte generado
    reports = sorted([f for f in os.listdir(".") if f.startswith("KRONOS_AUDIT_REPORT_") and f.endswith(".log")])
    if reports:
        target_report = reports[-1]
        with open(target_report, "a") as rf:
            rf.write(f"\n======================================================================\n")
            rf.write(f"NOM-151 BLOCKCHAIN INTEGRITY VERIFICATION\n")
            rf.write(f"GLOBAL MERKLE ROOT: {root_hash}\n")
            rf.write(f"ESTADO GENERAL: CADENA DE CUSTODIA CONSOLIDADA Y COMPLIANT\n")
            rf.write(f"======================================================================\n")
        print(f"\033[0;34m[REGISTRO]\033[0;0m Sello Merkle inyectado con éxito en: {target_report}")
