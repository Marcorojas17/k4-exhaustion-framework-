from PIL import Image
import numpy as np
import pathlib

def extract_matrix_from_png(path):
    """Tu base-0 magenta/cian -> matriz 2x2 Hill"""
    img = Image.open(path).convert("RGB")
    w,h = img.size
    quadrants = [
        img.crop((0,0,w//2,h//2)),
        img.crop((w//2,0,w,h//2)),
        img.crop((0,h//2,w//2,h)),
        img.crop((w//2,h//2,w,h))
    ]
    vals=[]
    for q in quadrants:
        r,g,b = np.array(q).mean(axis=(0,1))
        is_magenta = (r+b) > (g*1.2)
        vals.append(1 if is_magenta else 0)
    if vals == [0,0,0,0]:
        vals = [1,0,0,1]
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
