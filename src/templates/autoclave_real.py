from src.core.base_engine import BaseCryptoEngine

class AutoclaveRealEngine(BaseCryptoEngine):
    @property
    def name(self): return "AutoclaveReal"

    def decrypt(self, ct, key):
        primer, variant = key # variant: 'plain' o 'cipher'
        pt=[]
        key_stream = list(primer)
        for i,ch in enumerate(ct):
            c = ord(ch)-65
            if i < len(key_stream):
                k = ord(key_stream[i])-65
            else:
                if variant=='plain':
                    k = ord(pt[i-len(primer)])-65 if i>=len(primer) else 0
                else: # cipher autoclave
                    k = ord(ct[i-len(primer)])-65
            p = (c - k) % 26
            pt.append(chr(p+65))
            if variant=='plain':
                key_stream.append(chr(p+65))
            else:
                key_stream.append(ch) # ciphertext extiende
        return ''.join(pt)

    def get_key_generator(self):
        for primer in ["KRYPTOS","KRYPTOSABSTRA","PALIMPSEST","BERLIN","BERLINCLOCK","CIA","NSA"]:
            for var in ["plain","cipher"]:
                yield (primer,var)

