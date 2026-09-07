import os
from PIL import Image
from typing import List

class ImageKeyParser:
    """
    Procesa las 9 matrices de neón (0.png a 8.png) de la carpeta assets/
    traduciendo flujos visuales a bits criptográficos y coeficientes mod 26.
    """
    def __init__(self, assets_dir: str = "assets"):
        self.assets_dir = assets_dir
        self.name_map = {
            "matrix_1.png": "0.png",
            "matrix_2.png": "1.png",
            "matrix_3.png": "2.png",
            "matrix_4.png": "3.png",
            "matrix_5.png": "4.png",
            "matrix_6.png": "5.png",
            "matrix_7.png": "6.png",
            "matrix_8.png": "7.png",
            "matrix_9.png": "8.png"
        }

    def _resolve(self, filename: str) -> str:
        target_name = self.name_map.get(filename, filename)
        return os.path.join(self.assets_dir, target_name)

    def extract_bits_from_monochrome(self, filename: str) -> List[int]:
        path = self._resolve(filename)
        if not os.path.exists(path):
            return []
        with Image.open(path) as img:
            img = img.convert("1")
            pixels = list(img.getdata())
            return [0 if p == 0 else 1 for p in pixels]

    def extract_matrix_mod26(self, filename: str, size: int = 2) -> List[List[int]]:
        path = self._resolve(filename)
        if not os.path.exists(path):
            return []
        with Image.open(path) as img:
            img = img.convert("L")
            if img.size!= (size, size):
                img = img.resize((size, size))
            pixels = list(img.getdata())
            matrix = []
            for i in range(0, len(pixels), size):
                row = [p % 26 for p in pixels[i:i+size]]
                matrix.append(row)
            if len(matrix) == 1:
                return matrix[0]
            return matrix

    def parse_all_keys(self):
        return [os.path.join(self.assets_dir, f"{i}.png") for i in range(9) if os.path.exists(os.path.join(self.assets_dir, f"{i}.png"))]
