from src.templates.berlin_grille_vigenere import BerlinGrilleVigenereEngine
from src.core.fast_stats import fast_chi_squared
K4="OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
eng=BerlinGrilleVigenereEngine()
for key in eng.get_key_generator():
    pt=eng.decrypt(K4,key)
    chi=fast_chi_squared(pt)
    if "BERLIN" in pt or chi<70:
        print(f"HIT {chi:.1f} {pt} | {key}")
    else:
        print(f"{chi:.1f} | {key}")
