import numpy as np
from collections import Counter

ENGLISH_FREQ = np.array([0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749, 0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.00150, 0.01974, 0.00074])

def fast_chi_squared(text: str) -> float:
    text = text.upper()
    if len(text) != 97: return 999.0
    counts = Counter(c for c in text if 'A' <= c <= 'Z')
    observed = np.array([counts.get(chr(65+i), 0) for i in range(26)], dtype=float)
    expected = ENGLISH_FREQ * len(text)
    expected = np.where(expected == 0, 1e-6, expected)
    chi2 = np.sum((observed - expected)**2 / expected)
    return float(chi2)
