from src.templates.double_columnar_beaufort import DoubleColumnarBeaufortEngine
from src.core.fast_stats import fast_chi_squared

K4="OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
CRIB="BERLIN"
engine=DoubleColumnarBeaufortEngine()
best=[]
for key in engine.get_key_generator():
    try:
        pt=engine.decrypt(K4,key)
        chi=fast_chi_squared(pt)
        has_berlin = CRIB in pt[30:90] # ventana ampliada como sospechamos
        if has_berlin or chi<80:
            print(f"HIT! {chi:.1f} {pt} | {key} BERLIN={has_berlin}")
            best.append((chi,pt,key))
        else:
            print(f"{chi:.1f} {pt[:40]} | {key}")
    except Exception as e:
        print(f"err {e}")

print("\n=== FINAL ===")
for chi,pt,key in sorted(best)[:20]:
    print(chi,pt,key)
