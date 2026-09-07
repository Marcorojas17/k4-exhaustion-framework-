# src/data/generate_assets.py
import os
from PIL import Image

def generate_all_assets(output_dir="assets"):
    """
    Escribe de forma binaria y exacta los 9 PNGs en la carpeta assets/.
    Configura canales monocromáticos ('1') y escalas de grises ('L') 
    según lo requerido por ImageKeyParser.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"[*] Creando directorio físico de recursos: {output_dir}")

    # Estructura binaria de luces del Reloj de Berlín (23:51) -> 24 bits
    berlin_bits = [
        1, 1, 1, 1, 0,  # Fila 1 (Horas x5): 4 encendidas (20h)
        1, 1, 1, 0,     # Fila 2 (Horas x1): 3 encendidas (3h) -> Total 23h
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, # Fila 3 (Minutos x5): 10 encendidas (50m)
        1, 0, 0, 0      # Fila 4 (Minutos x1): 1 encendida (1m) -> Total 51m
    ]
    
    while len(berlin_bits) < 24:
        berlin_bits.append(0)

    # 1. Matrices Hill 2x2 (Escala de Grises - Canal 'L') - Mod 26 Invertibles
    m1 = Image.new("L", (2, 2))
    m1.putdata([3, 5, 1, 2])
    m1.save(os.path.join(output_dir, "matrix_1.png"))

    m2 = Image.new("L", (2, 2))
    m2.putdata([7, 3, 2, 1])
    m2.save(os.path.join(output_dir, "matrix_2.png"))

    # 2. Matrices de Transposición Columnar Asimétrica (4x25 y 4x86)
    m3 = Image.new("L", (25, 4))
    m3.putdata([i % 26 for i in range(100)])
    m3.save(os.path.join(output_dir, "matrix_3.png"))

    m4 = Image.new("L", (86, 4))
    m4.putdata([i % 26 for i in range(344)])
    m4.save(os.path.join(output_dir, "matrix_4.png"))

    # 3. Rejillas de Bits del Reloj de Berlín (Monocromático - Canal '1')
    offsets = [0, 8, 16]
    for idx, offset in enumerate(offsets, start=5):
        m_grid = Image.new("1", (8, 1))
        byte_segment = berlin_bits[offset:offset+8]
        pixel_values = [255 if bit == 1 else 0 for bit in byte_segment]
        m_grid.putdata(pixel_values)
        m_grid.save(os.path.join(output_dir, f"matrix_{idx}.png"))

    # 4. Máscara de retroalimentación LFSR (Polinomio x^24 + x^4 + x^3 + x + 1)
    m8 = Image.new("1", (24, 1))
    taps = [1 if i in [0, 1, 3, 23] else 0 for i in range(24)]
    m8.putdata([255 if t == 1 else 0 for t in taps])
    m8.save(os.path.join(output_dir, "matrix_8.png"))

    # 5. Tableau de Sustitución K1-K3 Completo (26x26 en Escala de Grises)
    m9 = Image.new("L", (26, 26))
    tableau = []
    for r in range(26):
        tableau.extend([(r + c) % 26 for c in range(26)])
    m9.putdata(tableau)
    m9.save(os.path.join(output_dir, "matrix_9.png"))

    print("[+] Las 9 matrices criptográficas PNG han sido depositadas con éxito en assets/.")

if __name__ == "__main__":
    generate_all_assets()
