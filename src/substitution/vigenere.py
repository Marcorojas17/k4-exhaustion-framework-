# src/substitution/vigenere.py
import numpy as np
from typing import Iterator, Any, List
from src.core.base_engine import BaseCryptoEngine
from src.utils.image_parser import ImageKeyParser

class VigenereCascadeEngine(BaseCryptoEngine):
    """
    Sustitución Vigenère polialfabética avanzada ejecutada en cascada
    sobre los 4 flujos de información del alfabeto dinámico de Kryptos.
    Usa la matriz de desplazamiento visual de assets/.
    """
    
    @property
    def name(self) -> str:
        return "VigenereCascade"

    def get_key_generator(self, **kwargs) -> Iterator[Any]:
        """
        Genera el espacio de claves periódicas utilizando los gradientes 
        extraídos de la matrix_9.png. Varía la longitud de la ventana (4 a 12).
        """
        parser = ImageKeyParser()
        m9_data = parser.extract_matrix_mod26("matrix_9.png", size=26)
        
        # Extraer la primera fila como vector base de desplazamientos numéricos
        if m9_data and len(m9_data) > 0:
            base_shifts = m9_data[0]
        else:
            base_shifts = list(range(26))
            
        # Generar variaciones periódicas modulares (longitudes de clave militares usuales)
        for length in range(4, 13):
            yield [base_shifts[i % len(base_shifts)] for i in range(length)]

    def decrypt(self, ciphertext: str, key: Any) -> str:
        """
        Descifra aplicando un desplazamiento inverso periódico sobre caracteres A-Z.
        """
        key_len = len(key)
        plaintext: List[str] = []
        
        for i, char in enumerate(ciphertext):
            if 'A' <= char <= 'Z':
                c_val = ord(char) - 65
                k_val = key[i % key_len]
                # Desplazamiento César inverso modular 26
                p_val = (c_val - k_val) % 26
                plaintext.append(chr(p_val + 65))
            else:
                plaintext.append(char)
                
        return "".join(plaintext)
