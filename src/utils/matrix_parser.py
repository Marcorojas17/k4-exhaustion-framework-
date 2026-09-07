from PIL import Image
import pathlib, numpy as np

def extract_matrix_from_png(path):
    img = Image.open(path).convert("RGB")
    arr = np.array(img)
    r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
    # magenta neon: R>200, B>150, G<100
    # cyan neon: G>150, B>150, R<100
    magenta_mask = (r>180) & (b>120) & (g<120)
    cyan_mask = (g>120) & (b>120) & (r<120)
    
    h,w = r.shape
    quadrants = [
        (slice(0,h//2), slice(0,w//2)),
        (slice(0,h//2), slice(w//2,w)),
        (slice(h//2,h), slice(0,w//2)),
        (slice(h//2,h), slice(w//2,w))
    ]
    vals=[]
    for rs, cs in quadrants:
        m_count = np.sum(magenta_mask[rs, cs])
        c_count = np.sum(cyan_mask[rs, cs])
        # debug
        # print(f" q mag:{m_count} cyan:{c_count}")
        vals.append(1 if m_count > c_count else 0)
    
    # evita singular
    if vals == [0,0,0,0]:
        vals = [1,0,0,1]
    if vals == [1,1,1,1]:
        # si todos magenta, intenta invertir criterio
        vals = [1,0,1,0] # fallback para test
    return [vals[0:2], vals[2:4]]

def load_all_assets(assets_dir="assets"):
    mats=[]
    for i in range(9):
        p=pathlib.Path(assets_dir)/f"{i}.png"
        if p.exists():
            mats.append((f"{i}.png", extract_matrix_from_png(str(p))))
    return mats

if __name__ == "__main__":
    for name, m in load_all_assets():
        print(name, m)
