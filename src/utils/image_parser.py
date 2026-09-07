import os
from PIL import Image
import numpy as np

class ImageKeyParser:
    def __init__(self, assets_dir="assets"):
        self.assets_dir = assets_dir

    def parse_all_keys(self):
        keys = {}
        if not os.path.exists(self.assets_dir):
            return keys
        for fname in sorted(os.listdir(self.assets_dir)):
            if not fname.endswith(".png"):
                continue
            if not fname[0].isdigit(): # solo 0.png - 8.png
                continue
            path = os.path.join(self.assets_dir, fname)
            try:
                img = Image.open(path).convert("L")
                keys[fname] = np.array(img)
            except Exception:
                continue
        return keys
