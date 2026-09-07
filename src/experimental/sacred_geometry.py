import math
import numpy as np
from src.core.base_engine import BaseCryptoEngine

class SacredGeometryEngine(BaseCryptoEngine):
    @property
    def name(self):
        return "SacredGeometry-LoShu"

    def get_key_generator(self, **kwargs):
        base_lo_shu = [4, 9, 2, 3, 5, 7, 8, 1, 6]
        matrix_3x3 = np.array(base_lo_shu).reshape(3, 3)
        for rot in range(4):
            r_matrix = np.rot90(matrix_3x3, rot)
            yield r_matrix.flatten().tolist()
            yield np.fliplr(r_matrix).flatten().tolist()

    def decrypt(self, ciphertext: str, key: list) -> str:
        alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        fib = [1, 1]
        for _ in range(len(ciphertext)):
            fib.append((fib[-1] + fib[-2]) % 26)
        plaintext = []
        key_len = len(key)
        for i, char in enumerate(ciphertext):
            if char in alpha:
                c_idx = alpha.index(char)
                geo_shift = fib[i] + key[i % key_len]
                p_idx = (c_idx - geo_shift) % 26
                plaintext.append(alpha[p_idx])
            else:
                plaintext.append(char)
        return "".join(plaintext)
