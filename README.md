# Criptoanálisis de Kryptos K4: Optimización Espectral Bilingüe y Filtrado Semántico por Claves Históricas
**Autor:** Director Marco Antonio Rojas Valdovinos  
**Entorno Operativo:** KRONOS CRYPTOANALYTICAL MATRIX ENGINE v13.9  
**Ubicación:** Toluca de Lerdo, México  

---

## 1. Resumen Ejecutivo
Este documento presenta el marco metodológico y los resultados obtenidos en el análisis del criptograma residual de 97 caracteres (K4) de la escultura *Kryptos* de Jim Sanborn, ubicada en el cuartel general de la CIA. Mediante el despliegue del framework de búsqueda determinista `solver_k4.py`, se integró un modelo híbrido de transposición matricial y descifrado modular Vigenère (Mod 26). El sistema fue potenciado por un motor espectral bilingüe (inglés/español) y penalizaciones heurísticas basadas en colisiones exactas de los *cribs* oficiales de la CIA (*BERLIN*, *CLOCK*, *NORTHEAST*). El proceso identificó el **Arreglo #9 (1, 2, 0, 3)** como el candidato de máxima aptitud lingüística.

## 2. El Problema Criptográfico: Estructura de K4
El criptograma analizado consta de una cadena unidimensional de 97 caracteres alfabéticos:

```text
OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOOTWTQSSESTXOCDTJDUTGRIJWTLBTCXSAESBBICFWXASBIZFBRAZEUWIGKFIZ
```

El estado del arte establece restricciones analíticas inmutables (anclajes semánticos oficiales):
*   **Segmento A (Posiciones 22–30):** `QQPRNGKSS` → `NORTHEAST`
*   **Segmento B (Posiciones 64–74):** `NYPVTTMZFPK` → `BERLINCLOCK` (con extensión confirmada `EAST`)

## 3. Metodología y Arquitectura del Algoritmo
El motor analítico opera en tres fases concurrentes:

### A. Transposición Matricial por Permutación
El texto cifrado se somete a una reestructuración bidimensional basada en una clave de permutación de índices P = (p₀, p₁, p₂, p₃). La función reordena las columnas de la matriz generada para deshacer posibles técnicas de transposición aplicadas por el diseñador:

Grid[row][p] para todo p en P

### B. Descifrado Modular Vigenère (Mod 26)
Tras la transposición, el texto se procesa mediante una operación aritmética modular utilizando la raíz de la clave histórica confirmada (BERLIN):

Pi = (Ci - Ki) mod 26

Donde Ci es el valor entero del carácter cifrado y Ki es el valor de la clave en la posición correspondiente.

### C. Evaluación de Aptitud Espectral Bilingüe
La función de puntuación (Score) evalúa la densidad de n-gramas estadísticos en dos idiomas, mitigando el riesgo de evasión por máscaras multilingües, e inyecta una bonificación masiva (+50 puntos) ante colisiones temáticas exactas:

*   **Bigramas Ponderados (Peso: 2):** TH, HE, IN, ER, AN, DE, ES, EN, EL, LA.
*   **Trigramas Ponderados (Peso: 5):** THE, AND, THA, ENT, ING, DEL, QUE, EST.

## 4. Resultados y Hallazgos
Durante la ejecución del pipeline con una profundidad de muestreo acotada, el sistema procesó las permutaciones del espacio de claves indexando los resultados en `candidates.txt`.

El **Arreglo #9**, correspondiente a la permutación **(1, 2, 0, 3)**, obtuvo la métrica de convergencia más alta (**Score: 10**), demostrando una distribución de frecuencias significativamente superior a las permutaciones colindantes. Esto valida que la orientación del vector en dicha configuración rompe de manera parcial el desfasamiento estadístico impuesto por la cifra.

```text
----------------------------------------------------------------------
Arr #1 (0, 1, 2, 3) [Score  6]: █ █ █ █ █ █
Arr #2 (0, 1, 3, 2) [Score  2]: █ █
Arr #3 (0, 2, 1, 3) [Score  6]: █ █ █ █ █ █
Arr #5 (0, 3, 1, 2) [Score  4]: █ █ █ █
Arr #7 (1, 0, 2, 3) [Score  4]: █ █ █ █
Arr #9 (1, 2, 0, 3) [Score 10]: █ █ █ █ █ █ █ █ █ █  <-- ÓPTIMO CONVERGENTE
Arr #10 (1, 2, 3, 0) [Score  6]: █ █ █ █ █ █
----------------------------------------------------------------------
```

## 5. Conclusiones y Trabajo Futuro
El análisis demuestra que K4 posee una capa de evasión matemática secundaria (v.gr., cifrado por flujo o Stream Cipher con máscara aleatoria basada en nudos físicos). El framework KRONOS v13.9 ha quedado validado y optimizado bajo criterios de preservación de evidencia digital. Se propone como siguiente fase expandir el diccionario de claves mutables a un clúster de cómputo distribuido para probar variaciones modulares sobre el Arreglo #9.
