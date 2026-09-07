from src.templates.beaufort_double_columnar import BeaufortDoubleColumnarEngine
from src.core.fast_stats import fast_chi_squared
K4="OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
engine=BeaufortDoubleColumnarEngine()
for key in engine.get_key_generator():
    pt=engine.decrypt(K4,key)
    chi=fast_chi_squared(pt)
    hit="BERLIN" in pt
    print(f"{chi:.1f} {pt[:45]} | {key} BERLIN={hit}")
