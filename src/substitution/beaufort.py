# src/substitution/beaufort.py
from typing import Iterator, Any, List
from src.core.base_engine import BaseCryptoEngine

class BeaufortEngine(BaseCryptoEngine):
    """
    Variante Beaufort estándar de la CIA donde la matemática es recíproca: 
    Texto Plano = (Clave - Criptograma) mod 26.
    """
    
    @property
    def name(self) -> str:
        return "Beaufort"

    def get_key_generator(self, **kwargs) -> Iterator[Any]:
        """
        Genera un espacio de claves estructuradas basado en palabras clave 
        históricas conocidas de la escultura Kryptos y pistas confirmadas.
        """
        base_keys = ["KRYPTOS", "PALIMPSEST", "BERLINCLOCK", "NORTHEAST", "SOUTHWEST"]
        for key in base_keys:
            yield [ord(c) - 65 for c in key.upper() if 'A' <= c <= 'Z']

    def decrypt(self, ciphertext: str, key: Any) -> str:
        """
        Descifra usando la transformación recíproca Beaufort de forma periódica.
        """
        key_len = len(key)
        plaintext: List[str] = []
        
        for i, char in enumerate(ciphertext):
            if 'A' <= char <= 'Z':
                c_val = ord(char) - 65
                k_val = key[i % key_len]
                # Ecuación matemática recíproca de Beaufort: (Key - Cipher) mod 26
                p_val = (k_val - c_val) % 26
                plaintext.append(chr(p_val + 65))
            else:
                plaintext.append(char)
                
        return "".join(plaintext)
