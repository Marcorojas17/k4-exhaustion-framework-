import os
from PIL import Image

def generate_all_neon_assets(output_dir="assets"):
    os.makedirs(output_dir, exist_ok=True)
    berlin_bits = [1,1,1,1,0,1,1,1,1,1,1,0,1,0,0,0]

    # 0.png Hill [[3,3],[2,5]]
    im=Image.new("L", (2,2)); im.putdata([3,3,2,5]); im.save(os.path.join(output_dir,"0.png"))
    im=Image.new("L", (2,2)); im.putdata([1,2,3,4]); im.save(os.path.join(output_dir,"1.png"))

    m2=Image.new("L", (25,4)); m2.putdata([i%26 for i in range(100)]); m2.save(os.path.join(output_dir,"2.png"))
    m3=Image.new("L", (86,4)); m3.putdata([i%26 for i in range(344)]); m3.save(os.path.join(output_dir,"3.png"))

    for idx, offset in enumerate([0,8,16]):
        if offset+8 <= len(berlin_bits):
            seg=berlin_bits[offset:offset+8]
        else:
            seg=berlin_bits[offset:] + [0]*(8-len(berlin_bits[offset:]))
        img=Image.new("1", (8,1))
        img.putdata([255 if b else 0 for b in seg])
        img.save(os.path.join(output_dir, f"{4+idx}.png"))
        print(f"{4+idx}.png -> {seg}")

    taps_pos=[0,1,3,4]
    taps=[1 if i in taps_pos else 0 for i in range(24)]
    im=Image.new("1", (24,1)); im.putdata([255 if t else 0 for t in taps]); im.save(os.path.join(output_dir,"7.png"))
    print(f"7.png -> {taps}")

    im=Image.new("L", (26,26)); im.putdata([(r+c)%26 for r in range(26) for c in range(26)]); im.save(os.path.join(output_dir,"8.png"))
    print("[+] 0.png-8.png listos")

generate_all_neon_assets()
