# src/templates/hill.py
import numpy as np
from typing import Iterator, Any, List
from src.core.base_engine import BaseCryptoEngine
from src.utils.image_parser import ImageKeyParser

class HillMatrixEngine(BaseCryptoEngine):
    """
    Cifrado Matricial Hill 2x2.
    Procesa bloques algebraicos mod 26. Extrae matrices candidatas de la topología 
    de matrix_1.png y matrix_2.png y calcula su matriz inversa modular para el descifrado.
    """
    
    @property
    def name(self) -> str:
        return "HillMatrix2x2"

    def get_key_generator(self, **kwargs) -> Iterator[Any]:
        """
        Genera el espacio de claves matriciales leyendo matrix_1 y matrix_2.
        Verifica la inversibilidad matemática mod 26 calculando el determinante y el inverso coprimo.
        """
        parser = ImageKeyParser()
        m1 = parser.extract_matrix_mod26("matrix_1.png", size=2)
        m2 = parser.extract_matrix_mod26("matrix_2.png", size=2)
        
        matrices_to_test = []
        if m1 and len(m1) == 2:
            matrices_to_test.append(np.array(m1))
        if m2 and len(m2) == 2:
            matrices_to_test.append(np.array(m2))
            
        # Fallback si no hay imágenes inicializadas en disco
        if not matrices_to_test:
            matrices_to_test.append(np.array([[3, 5], [1, 2]]))

        for A in matrices_to_test:
            # Calcular determinante numérico mod 26
            det = int(np.round(np.linalg.det(A))) % 26
            
            # Buscar el inverso multiplicativo modular del determinante (coprimo con 26)
            inv_det = -1
            for i in range(1, 26):
                if (det * i) % 26 == 1:
                    inv_det = i
                    break
                    
            if inv_det != -1:
                # Recomponer la matriz adjunta inversa modular 2x2:
                # [d, -b]
                # [-c, a]
                inv_A = np.array([[A[1, 1], -A[0, 1]], [-A[1, 0], A[0, 0]]])
                inv_A = (inv_det * inv_A) % 26
                yield inv_A
            else:
                # Fallback seguro con matriz invertible canónica de agencia
                yield np.array([[2, 5], [1, 3]])

    def decrypt(self, ciphertext: str, key: Any) -> str:
        """
        Descifra agrupando los caracteres A-Z en vectores columna de tamaño 2
        y multiplicándolos por la matriz inversa modular.
        """
        inv_matrix = key
        
        # Filtrar solo caracteres A-Z para la operación matricial lineal
        clean_chars = [c for c in ciphertext if 'A' <= c <= 'Z']
        if len(clean_chars) % 2 != 0:
            clean_chars.append('X') # Padding asimétrico estándar de bloques
            
        numeric_vector = np.array([ord(c) - 65 for c in clean_chars])
        decrypted_numeric: List[int] = []
        
        # Multiplicación matricial vectorial por bloques de tamaño 2
        for i in range(0, len(numeric_vector), 2):
            block = numeric_vector[i:i+2]
            res = np.dot(inv_matrix, block) % 26
            decrypted_numeric.extend(res.astype(int).tolist())
            
        # Recomponer la cadena manteniendo la integridad de los espacios y caracteres especiales
        idx = 0
        plaintext: List[str] = []
        for char in ciphertext:
            if 'A' <= char <= 'Z' and idx < len(decrypted_numeric):
                plaintext.append(chr(decrypted_numeric[idx] + 65))
                idx += 1
            else:
                plaintext.append(char)
                
        return "".join(plaintext)
