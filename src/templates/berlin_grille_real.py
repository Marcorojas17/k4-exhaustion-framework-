from src.core.base_engine import BaseCryptoEngine
import math

# Berlin Clock real: 4 filas: 4,4,11,4 luces
# Representamos BERLIN como patron de grille 7x14 = 98 ~ 97
def berlin_grille_mask(hour):
    # hour 0-23, genera mascara basada en Berlin Clock
    # Fila1: horas /5 (4 lamparas rojas)
    # Fila2: horas %5 (4 rojas)
    # Fila3: minutos /5 (11: 3 amarillas/rojas)
    # Fila4: minutos %5 (4 amarillas)
    # Simplificado: usamos binario de hour como agujeros
    mask=[]
    h=hour
    for i in range(14):
        for j in range(7):
            # patron rotante basado en hora
            if ((i*j + h) % 7 == 0) or ((i+j+h) % 5 ==0):
                mask.append(1)
            else:
                mask.append(0)
    return mask[:97]

class BerlinGrilleRealEngine(BaseCryptoEngine):
    @property
    def name(self): return "BerlinGrilleReal"

    def decrypt(self, ct, key):
        hour, rot = key # hour 0-23, rot 0-3 (90deg)
        mask = berlin_grille_mask(hour)
        # grille decryption: leer ct en orden de mascara
        pt=['']*97
        idx=0
        # aplicamos rotación simple a la grille
        for _ in range(rot):
            # rotate mask 90deg conceptual: shift
            mask = mask[7:] + mask[:7]
        for i,m in enumerate(mask):
            if m==1 and idx < len(ct):
                pt[i]=ct[idx]
                idx+=1
        # segunda pasada para huecos 0
        for i,m in enumerate(mask):
            if m==0 and idx < len(ct):
                pt[i]=ct[idx]
                idx+=1
        return ''.join(pt)

    def get_key_generator(self):
        for h in range(24):
            for rot in range(4):
                yield (h,rot)

