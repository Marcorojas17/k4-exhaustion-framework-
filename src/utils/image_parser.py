# src/utils/image_parser.py
import os
from PIL import Image
from typing import List

class ImageKeyParser:
    """Procesa los 9 PNG de assets/ para extraer estructuras criptográficas autónomas."""
    
    def __init__(self, assets_dir: str = "assets"):
        self.assets_dir = assets_dir

    def extract_bits_from_monochrome(self, filename: str) -> List[int]:
        """Convierte pixeles oscuros/claros en una cadena de bits (0s y 1s) para semillas LFSR."""
        path = os.path.join(self.assets_dir, filename)
        if not os.path.exists(path):
            return []
            
        with Image.open(path) as img:
            img = img.convert("1") # Forzar canal monocromático puro (Blanco y negro)
            pixels = list(img.getdata())
            # En formato Pillow de 1 bit: 0 representa negro, 255 representa blanco
            return [0 if p == 0 else 1 for p in pixels]

    def extract_matrix_mod26(self, filename: str, size: int = 2) -> List[List[int]]:
        """Mapea la luminosidad de los píxeles a valores 0-25 para matrices de Hill o transposición."""
        path = os.path.join(self.assets_dir, filename)
        if not os.path.exists(path):
            return []
            
        with Image.open(path) as img:
            img = img.convert("L") # Escala de grises pura
            # Asegurar redimensionamiento exacto a la cuadrícula matemática requerida
            img = img.resize((size, size) if img.size != (size, size) else img.size)
            pixels = list(img.getdata())
            
            matrix = []
            for i in range(0, len(pixels), size):
                row = [p % 26 for p in pixels[i:i+size]]
                matrix.append(row)
                
            # Si se solicita una sola fila (vector), simplificar la dimensión de salida
            if len(matrix) == 1:
                return matrix[0]
            return matrix
