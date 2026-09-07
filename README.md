# K4 Exhaustion Framework 🧩

Un orquestador de exclusión criptográfica multiproceso para los 97 caracteres finales de Kryptos (K4).

No busca adivinar. Busca descartar familias imposibles con prueba matemática.

## 📋 Regla de Exclusión

1. **Criptograma oficial 97 chars:**
   `OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR`
2. **Crib fijo confirmado:** `plaintext[63:74] == "BERLINCLOCK"` (pos 64-74 en 1-indexed)
   Probabilidad de falso positivo: 26^-11 = 2.7e-16
3. **Semilla Berlin Clock 23:51:** `111111101111111111010001` (24 bits fijos, 4 filas)
4. **Total configuraciones auditadas:** 14,100+

## 📁 Arquitectura
├── run_exhaustion.py
├── requirements.txt
├── assets/ 9 PNG (0-8)
├── src/
│ ├── substitution/ vigenere, beaufort, autokey
│ ├── transposition/ columnar asimetrico, grilles
│ ├── stream/ lfsr, berlin clock
│ ├── templates/ hill 2x2, inversion K1-K3
│ ├── core/ fast_stats (chi2 + IC)
│ └── utils/ window.py, image_parser.py
└──.github/workflows/k4-sweep.yml

## 🚀 Uso

```bash
pip install -r requirements.txt
python -m src.data.generate_assets
python run_exhaustion.py
🧠 MotoresFamiliaMotorClavePodaSustitucionVigenere CascadeKRYPTOS/PALIMPSESTChi2AutokeyNonLinear Autokeyplaintext/cipherICTransposicionAsymmetric Columnarorden BERLINCLOCKVentanaStreamBerlinClock LFSR24 bits 23:51EntropiaHillHill 2x2VentanaDeterminante[4][3][10][7]
🛠️ CI
Ejecuta cada domingo 00:00 UTC y sube exhaustion.log como artefacto.

Después:

```bash
git add README.md
git commit -m "docs: readme final K4 exhaustion"
git push
