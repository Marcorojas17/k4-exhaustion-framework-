# src/templates/inversion.py
from typing import Iterator, Any, List
from src.core.base_engine import BaseCryptoEngine
from src.utils.constants import K1_PLAINTEXT, K2_PLAINTEXT, K3_PLAINTEXT

class InversionTemplateEngine(BaseCryptoEngine):
    """
    Analiza K4 asumiendo herencia de plantillas o alfabetos inversos
    derivados matemáticamente de las soluciones conocidas de K1, K2 y K3.
    """
    
    @property
    def name(self) -> str:
        return "InversionTemplate"

    def get_key_generator(self, **kwargs) -> Iterator[Any]:
        """
        Genera combinaciones estructuradas de desfases moleculares entre 
        los fragmentos ya resueltos de la escultura.
        """
        known_texts = [K1_PLAINTEXT, K2_PLAINTEXT, K3_PLAINTEXT]
        for idx, text in enumerate(known_texts):
            clean_text = "".join([c for c in text.upper() if 'A' <= c <= 'Z'])
            if clean_text:
                yield (idx, clean_text)

    def decrypt(self, ciphertext: str, key: Any) -> str:
        """
        Descifra aplicando una inversión matemática recíproca modular periódica
        utilizando la plantilla de texto plano asignada.
        """
        idx, template = key
        template_len = len(template)
        plaintext: List[str] = []
        
        for i, char in enumerate(ciphertext):
            if 'A' <= char <= 'Z':
                c_val = ord(char) - 65
                t_val = ord(template[i % template_len]) - 65
                # Inversión matemática modular: (Template - Cipher) mod 26
                p_val = (26 + t_val - c_val) % 26
                plaintext.append(chr(p_val + 65))
            else:
                plaintext.append(char)
                
        return "".join(plaintext)
