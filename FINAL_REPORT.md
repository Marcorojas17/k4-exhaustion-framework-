# K4 Exhaustion - Negative Result (2026-09-07)
K4=OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR (97)
IC=0.0361 Random, Chi2=594.9 vs English

## Tested Models
- 11 engines orchestrator v2.0: 0 hits BERLIN, best english 92.0 SOTPYRK perm (3,2,4,6,1,5,0)
- Beaufort double columnar 48: best 364.8
- Berlin Grille 96: chi2 flat 576.5 = pure transposition, 0 BERLIN
- Grille+Vigenere 384: best 177.4 BERLIN key, 0 hits
- Berlin Clock LFSR 23 lights 192: best 320.9, 0 hits
- Autoclave KRYPTOS/PALIMPSEST/BERLIN/CIA/NSA plain+cipher 14: best 314.0, 0 hits

Total configs: 186,734
BERLIN hits in window 0-97: 0
English threshold <60: 0 pass

Conclusion: K4 is not pure transposition nor short-key polyalphabetic with Kryptos universe keys. Next: route+autoclave or external keystream.
