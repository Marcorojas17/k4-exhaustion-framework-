from src.utils.image_parser import ImageKeyParser
from src.utils.constants import K4_CIPHERTEXT

parser = ImageKeyParser("assets")
print("[*] Parsing Hill...")
m0 = parser.extract_matrix_mod26("0.png",2)
m1 = parser.extract_matrix_mod26("1.png",2)
print("Hill0",m0,"Hill1",m1)

print("[*] Bits Berlin...")
b4 = parser.extract_bits_from_monochrome("4.png")
b5 = parser.extract_bits_from_monochrome("5.png")
b6 = parser.extract_bits_from_monochrome("6.png")
print("B4",b4,"B5",b5,"B6",b6)

print("[*] LFSR...")
taps = parser.extract_bits_from_monochrome("7.png")
print("Taps",taps)

# Aquí enganchamos tu pipeline real
# Ej: Hill decrypt K4 con m0, luego transposición con 2.png/3.png
