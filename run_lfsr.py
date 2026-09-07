from src.templates.berlin_clock_lfsr_real import BerlinClockLFSRRealEngine
from src.core.fast_stats import fast_chi_squared
K4="OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
eng=BerlinClockLFSRRealEngine()
best=[]
for key in eng.get_key_generator():
    pt=eng.decrypt(K4,key)
    chi=fast_chi_squared(pt)
    hit="BERLIN" in pt
    line=f"{chi:.1f} {pt[:60]} | h={key[0]} m={key[1]} {key[2]} BERLIN={hit}"
    print(line)
    if hit or chi<80:
        best.append((chi,pt,key))

print("\n=== HITS ===")
for chi,pt,key in sorted(best)[:20]:
    print(chi,pt,key)
