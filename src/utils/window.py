def check_berlin_clock_window(pt: str, crib: str = "BERLINCLOCK", start: int = 63, end: int = 74) -> bool:
    """Regla de oro K4 - Ventana fija, no sliding. P = 26^-11"""
    if not pt or len(pt) != 97:
        return False
    if len(crib) != 11:
        return False
    return pt[start:end] == crib
