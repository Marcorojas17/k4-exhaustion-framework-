from typing import List, Tuple

def evaluate_crib_window(plaintext: str, cribs: List[str]) -> Tuple[int, str, int]:
    """
    Escáner deslizante dinámico sobre todo el espectro de la cadena descifrada.
    Busca coincidencias exactas o parciales de los cribs barriendo
    todas las posiciones posibles.
    """
    best_score = 0
    found_crib = "NONE"
    found_pos = -1

    for crib in cribs:
        crib_upper = crib.upper()
        crib_len = len(crib_upper)
        if len(plaintext) < crib_len:
            continue

        for pos in range(len(plaintext) - crib_len + 1):
            window_text = plaintext[pos:pos+crib_len].upper()
            matches = sum(1 for a, b in zip(window_text, crib_upper) if a == b)

            if matches > best_score:
                best_score = matches
                found_crib = crib_upper
                found_pos = pos

    if best_score >= 4:
        return best_score, found_crib, found_pos

    return 0, "NONE", -1
