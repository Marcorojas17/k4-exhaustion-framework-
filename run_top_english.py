from src.templates.vigenere_columnar_combo import VigenereColumnarComboEngine
from src.templates.hill_columnar_combo import HillColumnarComboEngine
from src.templates.hill import HillMatrixEngine
from src.core.fast_stats import fast_chi_squared
import heapq

K4 = "OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"

ENGINES = [
    ("HillColumnarCombo", HillColumnarComboEngine()),
    ("VigenereColumnarCombo", VigenereColumnarComboEngine()),
    ("HillMatrix2x2", HillMatrixEngine()),
]

TOP_N = 20
print(f"[*] Top English sin crib BERLIN")

for name, engine in ENGINES:
    print(f"\n=== {name} ===")
    heap = []
    count=0
    for key in engine.get_key_generator():
        try:
            pt = engine.decrypt(K4, key)
            chi = fast_chi_squared(pt)
            count+=1
            if len(heap) < TOP_N:
                heapq.heappush(heap, (-chi, pt[:97], str(key)[:100]))
            else:
                if chi < -heap[0][0]:
                    heapq.heappop(heap)
                    heapq.heappush(heap, (-chi, pt[:97], str(key)[:100]))
        except: continue
        if count % 10000 == 0:
            print(f" {count}...")
    results = sorted([(-c,p,k) for c,p,k in heap])
    for chi, pt, key in results:
        print(f"{chi:.1f} | {pt} | {key}")
    print(f"TOTAL {count} keys")
