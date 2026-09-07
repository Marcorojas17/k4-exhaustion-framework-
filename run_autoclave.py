from src.templates.autoclave_real import AutoclaveRealEngine
from src.core.fast_stats import fast_chi_squared
K4="OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
eng=AutoclaveRealEngine()
for key in eng.get_key_generator():
    pt=eng.decrypt(K4,key)
    chi=fast_chi_squared(pt)
    hit="BERLIN" in pt or "CLOCK" in pt
    print(f"{chi:.1f} {pt[:70]} | primer={key[0]} var={key[1]} HIT={hit}")
    if hit or chi<80:
        print(f"*** CANDIDATE {key} {pt}")

