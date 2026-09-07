# src/stream/lfsr.py
from typing import Iterator, Any, List
from src.core.base_engine import BaseCryptoEngine
from src.utils.image_parser import ImageKeyParser

class BerlinClockLFSREngine(BaseCryptoEngine):
    """
    Motor LFSR de 24 bits alimentado por las matrices de bits del Reloj de Berlín
    y la máscara de taps de assets/.
    """

    @property
    def name(self) -> str:
        return "BerlinClockLFSR"

    def get_key_generator(self, **kwargs) -> Iterator[Any]:
        """
        Genera el espacio de claves dinámico. Reconstruye el entero de 24 bits
        desde las matrices 5, 6 y 7, y barre una ventana temporal de 24 horas.
        """
        parser = ImageKeyParser()
        
        # Reconstruir los 24 bits desde las matrices monocromáticas de bytes
        bits_5 = parser.extract_bits_from_monochrome("matrix_5.png")
        bits_6 = parser.extract_bits_from_monochrome("matrix_6.png")
        bits_7 = parser.extract_bits_from_monochrome("matrix_7.png")
        
        base_seed_bits = bits_5 + bits_6 + bits_7
        if len(base_seed_bits) < 24:
            # Fallback estructural si las imágenes no se han inicializado en disco
            base_seed_bits = [
                1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 
                1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0
            ]

        # Convertir arreglo de bits en un entero puro de 24 bits
        seed_integer = 0
        for bit in base_seed_bits:
            seed_integer = (seed_integer << 1) | bit

        # Extraer la máscara de retroalimentación (polinomio de taps) de la matrix_8
        taps_bits = parser.extract_bits_from_monochrome("matrix_8.png")
        taps_mask = 0
        if taps_bits and len(taps_bits) >= 24:
            for bit in taps_bits:
                taps_mask = (taps_mask << 1) | bit
        else:
            # Polinomio canónico coprimo de agencia: x^24 + x^4 + x^3 + x + 1
            taps_mask = 0x80001D

        # Fuerza bruta dirigida: Barremos una ventana de 24 horas (86,400 segundos)
        # alrededor de la hora base para absorber desfases en el reloj físico
        for drift in range(-43200, 43200):
            yield ((seed_integer + drift) & 0xFFFFFF, taps_mask)

    def decrypt(self, ciphertext: str, key: Any) -> str:
        """
        Descifra corriendo el LFSR bit a bit para extraer bytes pseudoaleatorios,
        aplicando un desplazamiento César inverso mod 26.
        """
        seed, taps = key
        if seed == 0:
            seed = 1  # El estado nulo congelaría el registro de desplazamiento

        plaintext: List[str] = []
        state = seed

        for char in ciphertext:
            if not ('A' <= char <= 'Z'):
                plaintext.append(char)
                continue

            # Ciclo de reloj del LFSR de 24 bits para generar el flujo intermedio
            feedback = 0
            temp = state & taps
            while temp > 0:
                feedback ^= (temp & 1)
                temp >>= 1

            keystream_byte = state & 0xFF
            # Desplazar a la derecha e inyectar el bit de paridad en la posición superior (bit 23)
            state = ((state >> 1) | (feedback << 23)) & 0xFFFFFF

            # Criptoanálisis modular mod 26
            cipher_val = ord(char) - 65
            plain_val = (cipher_val - (keystream_byte % 26)) % 26
            plaintext.append(chr(plain_val + 65))

        return "".join(plaintext)
