import os
from PIL import Image

def generate_all_neon_assets(output_dir="assets"):
    os.makedirs(output_dir, exist_ok=True)
    print(f"[*] Creando directorio: {output_dir}")

    berlin_bits = [1,1,1,1,0,1,1,1,1,1,1,0,1,0,0,0]

    # 0.png, 1.png - Matrices Hill 2x2 mod26
    Image.new("L", (2,2)).putdata([3,3,2,5]).save(os.path.join(output_dir,"0.png"))
    Image.new("L", (2,2)).putdata([1,2,3,4]).save(os.path.join(output_dir,"1.png"))

    # 2.png, 3.png - Columnar 4x25 y 4x86
    m3 = Image.new("L", (25,4))
    m3.putdata([i % 26 for i in range(100)])
    m3.save(os.path.join(output_dir,"2.png"))

    m4 = Image.new("L", (86,4))
    m4.putdata([i % 26 for i in range(344)])
    m4.save(os.path.join(output_dir,"3.png"))

    # 4.png,5.png,6.png - Bytes Berlín
    offsets = [0,8,16]
    for target_idx, offset in enumerate(offsets, start=4):
        m_grid = Image.new("1", (8,1))
        byte_segment = berlin_bits[offset:offset+8]
        pixel_values = [255 if b==1 else 0 for b in byte_segment]
        m_grid.putdata(pixel_values)
        m_grid.save(os.path.join(output_dir, f"{target_idx}.png"))

    # 7.png - LFSR taps
    m8 = Image.new("1", (24,1))
    taps_pos = [0,1,3,4]
    taps = [1 if i in taps_pos else 0 for i in range(24)]
    m8.putdata([255 if t else 0 for t in taps])
    m8.save(os.path.join(output_dir,"7.png"))

    # 8.png - Tableau 26x26
    m9 = Image.new("L", (26,26))
    tableau = [(r+c)%26 for r in range(26) for c in range(26)]
    m9.putdata(tableau)
    m9.save(os.path.join(output_dir,"8.png"))

    print("[+] Sincronización exitosa. 0.png a 8.png listos.")

if __name__ == "__main__":
    generate_all_neon_assets()
