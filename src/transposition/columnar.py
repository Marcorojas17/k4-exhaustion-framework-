# src/transposition/columnar.py
import numpy as np
from typing import Iterator, Any, List
from src.core.base_engine import BaseCryptoEngine
from src.utils.image_parser import ImageKeyParser

class AsymmetricColumnarEngine(BaseCryptoEngine):
    """
    Motor de Transposición Columnar Asimétrica.
    Maneja matrices irregulares basadas en las dimensiones de Kryptos (4x25 y 4x86)
    derivando el orden de las columnas de los gradientes de los PNGs de assets/.
    """

    @property
    def name(self) -> str:
        return "AsymmetricColumnar"

    def get_key_generator(self, **kwargs) -> Iterator[Any]:
        """
        Genera el espacio de claves de permutación.
        Lee los vectores base de matrix_3 y matrix_4 y aplica desplazamientos (shifts)
        circulares para buscar la alineación correcta.
        """
        parser = ImageKeyParser()

        # Extraer filas guía de las imágenes de transposición
        m3_pixels = parser.extract_matrix_mod26("matrix_3.png", size=25)
        m4_pixels = parser.extract_matrix_mod26("matrix_4.png", size=86)

        # Usamos la primera fila de cada imagen como la "palabra clave" numérica de permutación
        base_key_25 = m3_pixels[0] if (m3_pixels and len(m3_pixels) > 0) else list(range(25))
        base_key_86 = m4_pixels[0] if (m4_pixels and len(m4_pixels) > 0) else list(range(86))

        # El iterador prueba diferentes anchos de columna (frecuentes en K1-K3 como 4, 8, 25, 86)
        # y variaciones de permutación basadas en desplazamientos criptográficos
        for width in [4, 8, 25, 86]:
            if width <= 25:
                current_base = base_key_25[:width]
            else:
                current_base = base_key_86[:width]

            # Generar variaciones por rotación de clave (fuerza bruta dirigida)
            for shift in range(width):
                mutated_key = np.roll(current_base, shift).tolist()
                yield (width, mutated_key)

    def decrypt(self, ciphertext: str, key: Any) -> str:
        """
        Descifra una transposición columnar asimétrica (irregular).
        Reconstruye las columnas respetando los caracteres sobrantes al final.
        """
        width, col_pattern = key
        num_chars = len(ciphertext)

        # Calcular dimensiones de la cuadrícula
        full_rows = num_chars // width
        remainder = num_chars % width

        # Determinar cuántos caracteres tiene exactamente cada columna
        # El orden de las columnas viene dado por el rango ordenado de col_pattern
        col_order = sorted(range(width), key=lambda k: col_pattern[k])

        col_lengths = [full_rows] * width
        for i in range(remainder):
            col_lengths[i] += 1 # Las primeras columnas reciben el remanente asimétrico

        # Reconstruir las columnas desde el criptograma
        columns_data = {}
        idx = 0
        for col_idx in col_order:
            length = col_lengths[col_idx]
            columns_data[col_idx] = ciphertext[idx:idx+length]
            idx += length

        # Leer la cuadrícula fila por fila para obtener el texto plano
        plaintext_list: List[str] = []
        for r in range(full_rows + (1 if remainder > 0 else 0)):
            for c in range(width):
                if r < len(columns_data[c]):
                    plaintext_list.append(columns_data[c][r])

        return "".join(plaintext_list)
