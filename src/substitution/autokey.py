# src/substitution/autokey.py
from typing import Iterator, Any, List
from src.core.base_engine import BaseCryptoEngine

class NonLinearAutokeyEngine(BaseCryptoEngine):
    """
    Autoclave de alimentación mixta no lineal. Rompe los ataques automáticos de 
    Friedman al alternar dinámicamente entre alimentar la clave con el texto plano 
    o el criptograma según la paridad de la posición.
    """
    
    @property
    def name(self) -> str:
        return "NonLinearAutokey"

    def get_key_generator(self, **kwargs) -> Iterator[Any]:
        """
        Genera semillas de inicialización (Priming Keys) de 4 a 6 caracteres
        derivadas de términos estructurales confirmados por Sanborn.
        """
        priming_options = ["KRYP", "BERL", "CLOC", "PALI", "EDSCH", "SCHEIDT"]
        for p in priming_options:
            yield [ord(c) - 65 for c in p.upper() if 'A' <= c <= 'Z']

    def decrypt(self, ciphertext: str, key: Any) -> str:
        """
        Descifra la secuencia inyectando asimétricamente los caracteres intermedios
        al flujo de la clave dinámica en tiempo de ejecución.
        """
        current_key = list(key)
        plaintext: List[str] = []
        
        for i, char in enumerate(ciphertext):
            if 'A' <= char <= 'Z':
                c_val = ord(char) - 65
                k_val = current_key[i]
                # Descifrado básico Vigenère para la posición actual
                p_val = (c_val - k_val) % 26
                plain_char = chr(p_val + 65)
                plaintext.append(plain_char)
                
                # Regla No Lineal: Inyección asimétrica a la secuencia de autoclave
                if (i % 2) == 0:
                    current_key.append(p_val) # Realimentación del texto plano
                else:
                    current_key.append(c_val) # Realimentación del criptograma
            else:
                plaintext.append(char)
                # Mantener la alineación del flujo de la clave ante caracteres especiales
                current_key.append(0)
                
        return "".join(plaintext)
