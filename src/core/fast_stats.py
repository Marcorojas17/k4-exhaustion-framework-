# src/core/fast_stats.py
import numpy as np

# Perfil estadístico de frecuencias esperadas para el idioma inglés estándar (A-Z)
ENGLISH_FREQ = np.array([
    0.0817, 0.0149, 0.0278, 0.0425, 0.1270, 0.0223, 0.0202, 0.0609, 0.0697, 
    0.0015, 0.0077, 0.0403, 0.0241, 0.0675, 0.0751, 0.0193, 0.0010, 0.0599, 
    0.0633, 0.0906, 0.0276, 0.0098, 0.0236, 0.0015, 0.0197, 0.0007
])

def fast_chi_squared(text: str) -> float:
    """
    Calcula la prueba estadística Chi-cuadrado a alta velocidad mediante vectorización.
    Compara las frecuencias observadas contra la distribución natural del inglés.
    Valores más bajos indican una estructura lingüística real (legible).
    """
    # Convertir el texto plano a un buffer numérico ASCII de alta velocidad
    encoded = np.frombuffer(text.encode('ascii', errors='ignore'), dtype=np.uint8)
    
    # Máscara booleana para retener únicamente letras mayúsculas válidas (A=65, Z=90)
    mask = (encoded >= 65) & (encoded <= 90)
    encoded = encoded[mask] - 65
    
    n = len(encoded)
    if n == 0:
        return float('inf')
        
    # Conteo optimizado de frecuencias por cubo (minlength=26 para asegurar el alfabeto)
    observed = np.bincount(encoded, minlength=26)
    expected = ENGLISH_FREQ * n
    
    # Operación matemática vectorial directa en hardware
    chi2 = np.sum(((observed - expected) ** 2) / expected)
    return float(chi2)
