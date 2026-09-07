# src/transposition/grilles.py
import numpy as np
from typing import Iterator, Any, List
from src.core.base_engine import BaseCryptoEngine
from src.utils.image_parser import ImageKeyParser

class BerlinGrilleEngine(BaseCryptoEngine):
    """
    Transposición por Rejilla Giratoria Asimétrica.
    Utiliza los mapas de bits de las matrices 5 y 6 para perforar huecos 
    sobre una cuadrícula física de Kryptos y rota en pasos de 90 grados.
    """
    
    @property
    def name(self) -> str:
        return "BerlinGrille"

    def get_key_generator(self, **kwargs) -> Iterator[Any]:
        """
        Genera el espacio de claves combinando los bits base del Reloj de Berlín
        con las 4 fases de rotación geométrica (0, 90, 180, 270 grados).
        """
        parser = ImageKeyParser()
        b5 = parser.extract_bits_from_monochrome("matrix_5.png")
        b6 = parser.extract_bits_from_monochrome("matrix_6.png")
        
        # Combinar flujos binarios de los bytes del reloj para formar la máscara 4x4 (16 posiciones)
        mask = (b5 + b6)[:16] if (b5 and b6) else []
        if len(mask) < 16:
            # Fallback seguro con máscara simétrica balanceada si no hay imágenes
            mask = [1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1]
            
        for rotations in range(4):
            yield (mask, rotations)

    def decrypt(self, ciphertext: str, key: Any) -> str:
        """
        Descifra aplicando la plantilla de la rejilla rotada por bloques iterativos
        y reorganiza los caracteres según la posición de las perforaciones.
        """
        mask, rotations = key
        size = 4 # Dimensión de la cuadrícula interna de 4x4 para fragmentar K4
        grid_mask = np.array(mask).reshape(size, size)
        
        # Aplicar la rotación matricial vectorial de NumPy según la fase de la clave
        grid_mask = np.rot90(grid_mask, rotations)
        
        length = len(ciphertext)
        output: List[str] = [''] * length
        
        cipher_idx = 0
        # Procesar secuencialmente a través de bloques de 16 caracteres
        for block_start in range(0, length, size * size):
            for r in range(size):
                for c in range(size):
                    if grid_mask[r, c] == 1 and cipher_idx < length:
                        target_pos = block_start + (r * size + c)
                        if target_pos < length:
                            output[target_pos] = ciphertext[cipher_idx]
                            cipher_idx += 1
                            
        # Rellenar los huecos asimétricos restantes con transposición lineal directa
        for i in range(length):
            if output[i] == '' and cipher_idx < length:
                output[i] = ciphertext[cipher_idx]
                cipher_idx += 1
                
        return "".join(output)
