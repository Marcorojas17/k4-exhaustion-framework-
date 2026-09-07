import os
from PIL import Image
from typing import List

class ImageKeyParser:
    def __init__(self, assets_dir="assets"):
        self.assets_dir = assets_dir
        # Mapeo legacy -> base-0 web
        self.name_map = {
            "matrix_1.png": "0.png",
            "matrix_2.png": "1.png",
            "matrix_3.png": "2.png",
            "matrix_4.png": "3.png",
            "matrix_5.png": "4.png",
            "matrix_6.png": "5.png",
            "matrix_7.png": "6.png",
            "matrix_8.png": "7.png",
            "matrix_9.png": "8.png",
        }

    def _resolve(self, filename: str) -> str:
        target = self.name_map.get(filename, filename)
        return os.path.join(self.assets_dir, target)

    def parse_all_keys(self):
        keys = []
        for i in range(9):
            p = os.path.join(self.assets_dir, f"{i}.png")
            if os.path.exists(p):
                keys.append(p)
        return keys

    def extract_bits_from_monochrome(self, filename: str) -> List[int]:
        path = self._resolve(filename)
        img = Image.open(path).convert('1')
        return [1 if px else 0 for px in img.getdata()]

    def extract_matrix_mod26(self, filename: str, size: int = 2) -> List[List[int]]:
        path = self._resolve(filename)
        img = Image.open(path).convert('L')
        data = list(img.getdata())
        # reconstruye matriz size x size
        return [data[i*size:(i+1)*size] for i in range(size)]

