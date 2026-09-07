# K4 - Exclusión Final Modelos Clásicos (2026-09-07)

## Método
Orquestador v2.0, 2 cores, K4=97 chars, CHI2_MAX=120, crib BERLIN ventana 60:85

## Resultados 11 motores
0 hits. Log: exhaustion.log

## Top English sin crib
- VigenereColumnarCombo: 92.0 SOTPYRK (KRYPTOS rev) perm (3,2,4,6,1,5,0)
- HillColumnarCombo: 107.0
Umbral inglés legible: <60 -> NO PASA

## Double Columnar + Beaufort (intuición)
- Orden C->B: mejor 364.8
- Orden B->C: mejor 409.3
0 hits BERLIN en ventana ampliada 0-97

## Conclusión
Se descarta solución simple basada solo en transposición columnar + Vigenère/Beaufort
con claves KRYPTOS/PALIMPSEST/BERLIN/CLOCK. Siguiente fase debe probar:
- Máscara irregular (grille)
- Route transposition
- One-time pad con Berlin Clock real como keystream
