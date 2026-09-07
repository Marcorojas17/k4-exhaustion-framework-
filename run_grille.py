from src.templates.berlin_grille_real import BerlinGrilleRealEngine
from src.core.fast_stats import fast_chi_squared
K4="OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
engine=BerlinGrilleRealEngine()
best=[]
for key in engine.get_key_generator():
    pt=engine.decrypt(K4,key)
    chi=fast_chi_squared(pt)
    has_berlin="BERLIN" in pt
    print(f"{chi:.1f} {pt[:50]} | hour={key[0]} rot={key[1]} BERLIN={has_berlin}")
    if has_berlin or chi<80:
        best.append((chi,pt,key))

print("\n=== HITS ===")
for chi,pt,key in sorted(best)[:10]:
    print(chi,pt,key)
