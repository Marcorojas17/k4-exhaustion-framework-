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
        for fname in os.listdir(self.assets_dir):
            if fname.endswith(".png"):
                path = os.path.join(self.assets_dir, fname)
                img = Image.open(path).convert("L")
                keys[fname] = np.array(img)
        return keys
