masks=[
[[0,1,1,1],[0,0,0,0],[0,1,1,1],[0,1,1,1]], #0
[[1,1,1,1],[0,0,0,0],[0,1,1,1]], #1
[[1,0,1,1],[1,0,0,0],[1,0,0,0]], #2
[[1,0,1,1],[1,0,0,0]], #3
[[0,0,0,0],[1,1,1,0],[1,1,1,0]], #4
[[1,1,1,1],[1,0,0,0],[0,1,1,1],[0,1,1,1]], #5
[[1,0,1,1],[1,0,0,0],[1,0,1,1]], #6
[[1,1,0,1],[1,1,0,1],[1,0,0,0],[0,0,0,0]], #7
[[0,1,1,1],[0,0,0,0]], #8
]
# aplanar en orden 0-8
order=[]
for m in masks:
    for r in range(4):
        for c in range(4):
            if m[r][c]==1:
                order.append((m,r,c))

print(f"Activos totales: {len(order)}") # deberia ~?
# Usa primeros 97 activos como grille de lectura
K4="OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
# Prueba: reordenar K4 según order
# Mapea ct a posiciones activas
from src.core.fast_stats import fast_chi_squared
# generar pt leyendo en orden de activos
pt_list=['']*97
for i, pos in enumerate(order[:97]):
    pt_list[i]=K4[i] # placeholder - aqui va logica real de grille

# Te armo el engine real si me confirmas el orden de lectura:
# ¿Lee 0->8 en filas, o columnas? ¿MAGENTA primero luego CIAN?
