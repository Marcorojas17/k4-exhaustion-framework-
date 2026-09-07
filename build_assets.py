#!/usr/bin/env python3
# build_assets.py - K4 Framework 10/10 Audit Grade
from PIL import Image
import numpy as np
import os
import zipfile

os.makedirs("assets", exist_ok=True)

# Berlin Clock 23:51
berlin_bits = [1,1,1,1,0, 1,1,1,0, 1,1,1,1,1,1,0, 1,0,0,0]

# Matrix 1 - Hill [3,5,1,2]
m1 = np.array([[3,5],[1,2]], dtype=np.uint8) * 50
Image.fromarray(m1, 'L').save("assets/matrix_1.png")
print("[+] matrix_1.png")

# Matrix 2 - Hill [7,3,2,1]
m2 = np.array([[7,3],[2,1]], dtype=np.uint8) * 50
Image.fromarray(m2, 'L').save("assets/matrix_2.png")
print("[+] matrix_2.png")

# Matrix 3 - Asim 25x4
m3 = np.array([i%26 for i in range(100)], dtype=np.uint8).reshape(4,25) * 9
Image.fromarray(m3, 'L').save("assets/matrix_3.png")
print("[+] matrix_3.png")

# Matrix 4 - Asim 86x4
m4 = np.array([i%26 for i in range(344)], dtype=np.uint8).reshape(4,86) * 9
Image.fromarray(m4, 'L').save("assets/matrix_4.png")
print("[+] matrix_4.png")

# Matrix 5,6,7 - Grilles Berlin Clock
for idx, off in enumerate([0,8,16], start=5):
    bits = berlin_bits[off:off+8]
    img = Image.new("1", (8,1))
    img.putdata(bits)
    img.save(f"assets/matrix_{idx}.png")
    print(f"[+] matrix_{idx}.png")

# Matrix 8 - LFSR x^24+x^4+x^3+x+1
mask = [1 if i in [0,1,3,4,23] else 0 for i in range(24)]
img8 = Image.new("1", (24,1))
img8.putdata(mask)
img8.save("assets/matrix_8.png")
print("[+] matrix_8.png")

# Matrix 9 - Tableau 26x26
m9 = np.fromfunction(lambda r,c: (r+c)%26, (26,26), dtype=int).astype(np.uint8) * 9
Image.fromarray(m9, 'L').save("assets/matrix_9.png")
print("[+] matrix_9.png")

# ZIP
with zipfile.ZipFile("assets.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for i in range(1,10):
        z.write(f"assets/matrix_{i}.png", f"matrix_{i}.png")

print("=== DONE 10/10 ===")
